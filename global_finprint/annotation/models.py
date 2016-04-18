from django.db import models
from django.contrib.gis.db import models as geomodels

from global_finprint.core.models import AuditableModel, FinprintUser
from global_finprint.habitat.models import Region

ANIMAL_SEX_CHOICES = {
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Unknown'),
}
ANIMAL_STAGE_CHOICES = {
    ('AD', 'Adult'),
    ('JU', 'Juvenile'),
    ('U', 'Unknown'),
}
OBSERVATION_TYPE_CHOICES = {
    ('I', 'Of interest'),
    ('A', 'Animal'),
}


class AnimalGroup(models.Model):
    name = models.CharField(max_length=24)

    def __str__(self):
        return u"{0}".format(self.name)


class Animal(models.Model):
    regions = models.ManyToManyField(Region)
    rank = models.PositiveIntegerField(null=True, blank=True)
    group = models.ForeignKey(to=AnimalGroup)
    common_name = models.CharField(max_length=100)
    family = models.CharField(max_length=100)
    genus = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    fishbase_key = models.IntegerField(null=True, blank=True)
    sealifebase_key = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('genus', 'species')

    @staticmethod
    def get_for_api(assignment):
        return list(a.to_json() for a in assignment.video.set.trip.region.animal_set.all())

    def to_json(self):
        return {
            'id': self.id,
            'rank': self.rank,
            'group': str(self.group),
            'group_id': self.group_id,
            'common_name': self.common_name,
            'family': self.family,
            'genus': self.genus,
            'species': self.species,
            'fishbase_key': self.fishbase_key,
            'sealifebase_key': self.sealifebase_key,
            'regions': list({'id': r.id, 'region': str(r)} for r in self.regions.all())
        }

    def __str__(self):
        return u"{0} ({1} {2})".format(self.common_name, self.genus, self.species)


class AnimalBehavior(models.Model):
    #    swim by, stimulated, interaction
    type = models.CharField(max_length=16)

    def __str__(self):
        return u"{0}".format(self.type)


class Video(AuditableModel):
    file = models.CharField(max_length=100, null=True, blank=True)

    def annotators_assigned(self):
        return Assignment.objects.filter(video=self).exclude(status=5)

    def __str__(self):
        return u"{0}".format(self.file)


# 1 = Not Started, 2 = In progress, 3 = Ready for review
# 4 = Completed, 5 = Disabled, 6 = Rejected
class AnnotationState(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return u'{0}'.format(self.name)

    class Meta:
        ordering = ['id']


class Assignment(AuditableModel):
    annotator = models.ForeignKey(to=FinprintUser)
    video = models.ForeignKey(to=Video)
    assigned_by = models.ForeignKey(to=FinprintUser, related_name='assigned_by')
    status = models.ForeignKey(to=AnnotationState, default=1)
    progress = models.IntegerField(default=0)

    def set(self):
        return self.video.set

    def update_progress(self, seconds):
        if seconds > self.progress:
            self.progress = seconds
            self.save()
        return self.progress

    @classmethod
    def get_active(cls):
        return cls.objects.filter(status_id__in=[1, 2])

    @classmethod
    def get_active_for_annotator(cls, annotator):
        return cls.get_active().filter(annotator=annotator)

    def to_json(self):
        return {'id': self.id,
                'set_code': str(self.set()),
                'file': str(self.video.file),
                'assigned_to': {'id': self.annotator.id, 'user': str(self.annotator)},
                'progress': self.progress}


class ObservationFeature(models.Model):
    id = models.AutoField(primary_key=True)
    feature = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return u"{0}".format(self.feature)


class Observation(AuditableModel):
    assignment = models.ForeignKey(Assignment)
    type = models.CharField(max_length=1, choices=OBSERVATION_TYPE_CHOICES, default='I')
    initial_observation_time = models.IntegerField(help_text='ms')
    duration = models.PositiveIntegerField(null=True, blank=True)
    comment = models.CharField(max_length=256, null=True)
    extent = geomodels.PolygonField(null=True)
    created_by = models.ForeignKey(to=FinprintUser, related_name='observations_created', null=True)
    updated_by = models.ForeignKey(to=FinprintUser, related_name='observations_updated', null=True)

    @staticmethod
    def create(**kwargs):
        kwargs['initial_observation_time'] = int(kwargs['initial_observation_time'])
        kwargs['type'] = kwargs.pop('type_choice', None)
        kwargs['created_by'] = kwargs['user'].finprintuser
        kwargs['updated_by'] = kwargs['user'].finprintuser

        animal_fields = {
            'animal_id': kwargs.pop('animal_id', None),
            'sex': kwargs.pop('sex_choice', None),
            'stage': kwargs.pop('stage_choice', None),
            'length': kwargs.pop('length', None),
            'behaviors': kwargs.pop('behavior_ids', None),
            'features': kwargs.pop('feature_ids', None),
            'user': kwargs['user']
        }
        animal_fields = dict((k, v) for k, v in animal_fields.items() if v is not None)

        obs = Observation(**kwargs)
        obs.save()

        if kwargs.get('type') == 'A':
            behaviors = animal_fields.pop('behaviors', None)
            features = animal_fields.pop('features', None)

            animal_fields['observation'] = obs
            animal_obs = AnimalObservation(**animal_fields)
            animal_obs.save()

            animal_obs.behaviors = [] if behaviors is None else list(int(b) for b in behaviors.split(','))
            animal_obs.features = [] if features is None else list(int(f) for f in features.split(','))
            animal_obs.save()

        return obs

    @staticmethod
    def valid_fields():
        return [
            'type_choice',
            'initial_observation_time',
            'duration',
            'extent',
            'comment',
            'animal_id',
            'sex_choice',
            'stage_choice',
            'length',
            'behavior_ids',
            'feature_ids',
        ]

    @classmethod
    def get_for_api(cls, assignment):
        return list(ob.to_json() for ob in cls.objects.filter(assignment=assignment))

    def set(self):
        return self.assignment.video.set

    def to_json(self):
        json = {
            'id': self.id,
            'type': self.get_type_display(),
            'type_choice': self.type,
            'initial_observation_time': self.initial_observation_time,
            'duration': self.duration,
            'extent': None if self.extent is None else str(self.extent),
            'comment': self.comment,
        }

        if self.type == 'A':
            animal = self.animalobservation
            json.update({
                'animal': str(animal.animal),
                'animal_id': animal.animal_id,
                'sex': animal.get_sex_display(),
                'sex_choice': animal.sex,
                'stage': animal.get_stage_display(),
                'stage_choice': animal.stage,
                'length': animal.length,
                'behaviors': list({'id': b.pk, 'type': b.type} for b in animal.behaviors.all()),
                'features': list({'id': f.pk, 'feature': f.feature} for f in animal.features.all()),
            })

        return json

    def __str__(self):
        return u"{0}".format(self.initial_observation_time)


class AnimalObservation(AuditableModel):
    observation = models.OneToOneField(to=Observation)
    animal = models.ForeignKey(Animal)
    sex = models.CharField(max_length=1,
                           choices=ANIMAL_SEX_CHOICES, default='U')
    stage = models.CharField(max_length=2,
                             choices=ANIMAL_STAGE_CHOICES, default='U')
    length = models.IntegerField(null=True, help_text='centimeters')
    behaviors = models.ManyToManyField(to=AnimalBehavior)
    features = models.ManyToManyField(to=ObservationFeature)

    def behavior_display(self):
        return list()


class Image(AuditableModel):
    # todo:  placeholder!  this should be filesystem / S3 ...
    name = models.FileField()

    class Meta:
        abstract = True


class ObservationImage(Image):
    # todo:  placeholder!
    video = models.ForeignKey(Video)
    observation = models.ForeignKey(Observation)


class SiteImage(Image):
    # todo:  placeholder!
    video = models.ForeignKey(Video)

    def set(self):
        return self.video.set

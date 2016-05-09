from django.db import models
from django.contrib.gis.db import models as geomodels

from global_finprint.core.models import AuditableModel, FinprintUser

from .video import Assignment
from .animal import Animal, ANIMAL_SEX_CHOICES, ANIMAL_STAGE_CHOICES
from .annotation import AnimalBehavior, ObservationFeature


OBSERVATION_TYPE_CHOICES = {
    ('I', 'Of interest'),
    ('A', 'Animal'),
}


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
    features = models.ManyToManyField(to=ObservationFeature)
    behaviors = models.ManyToManyField(to=AnimalBehavior)

    def behavior_display(self):
        return list()

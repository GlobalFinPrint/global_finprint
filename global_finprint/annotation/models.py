from django.db import models

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
VIDEO_ANNOTATOR_CHOICES = {
    ('N', 'Not started'),
    ('I', 'In progress'),
    ('C', 'Competed')
}


class AnimalGroup(models.Model):
    name = models.CharField(max_length=24)

    def __str__(self):
        return u"{0}".format(self.name)


class Animal(models.Model):
    regions = models.ManyToManyField(Region)
    rank = models.PositiveIntegerField()
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
    def get_for_api(video_annotator):
        return list(a.to_json() for a in video_annotator.video.set.trip.region.animal_set.all())

    def to_json(self):
        return {
            'id': self.id,
            'rank': self.rank,
            'group': str(self.group),
            'common_name': self.common_name,
            'family': self.family,
            'genus': self.genus,
            'species': self.species,
            'fishbase_key': self.fishbase_key,
            'sealifebase_key': self.sealifebase_key
        }

    def __str__(self):
        return u"{0} {1} ({2})".format(self.genus, self.species, self.common_name)


class AnimalBehavior(models.Model):
    #    swim by, stimulated, interaction
    type = models.CharField(max_length=16)

    def __str__(self):
        return u"{0}".format(self.type)


class Video(AuditableModel):
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return u"{0}".format(self.file)


class Lead(FinprintUser):
    pass


class Annotator(FinprintUser):
    pass


class VideoAnnotator(AuditableModel):
    annotator = models.ForeignKey(to=Annotator)
    video = models.ForeignKey(to=Video)
    assigned_by = models.ForeignKey(to=Lead, related_name='assigned_by')
    status = models.CharField(max_length=1, choices=VIDEO_ANNOTATOR_CHOICES, default='N')


class Observation(AuditableModel):
    initial_observation_time = models.DurationField(help_text='ms')

    animal = models.ForeignKey(Animal)
    sex = models.CharField(max_length=1,
                           choices=ANIMAL_SEX_CHOICES, default='U')
    stage = models.CharField(max_length=2,
                             choices=ANIMAL_STAGE_CHOICES, default='U')
    length = models.IntegerField(null=True, help_text='centimeters')

    behavior = models.ForeignKey(to=AnimalBehavior, null=True)
    duration = models.PositiveIntegerField()
    comment = models.CharField(max_length=256, null=True)

    video_annotator = models.ForeignKey(VideoAnnotator)

    @classmethod
    def get_for_api(cls, video_annotator):
        return list(ob.to_json() for ob in cls.objects.filter(video_annotator=video_annotator))

    def set(self):
        return self.video_annotator.video.set

    def to_json(self):
        return {
            'id': self.id,
            'initial_observation_time': (self.initial_observation_time.total_seconds() * 1000),
            'animal': str(self.animal),
            'sex': self.get_sex_display(),
            'stage': self.get_stage_display(),
            'length': self.length,
            'behavior': str(self.behavior),
            'duration': self.duration,
            'comment': self.comment
        }

    def __str__(self):
        return u"{0}".format(self.initial_observation_time.total_seconds() * 1000)


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

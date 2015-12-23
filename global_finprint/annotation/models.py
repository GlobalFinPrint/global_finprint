from django.db import models
from django.contrib.auth.models import User
from django.apps import apps

from global_finprint.core.models import AuditableModel
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

    def __str__(self):
        return u"{0} {1} ({2})".format(self.genus, self.species, self.common_name)


class AnimalBehavior(models.Model):
    #    swim by, stimulated, interaction
    type = models.CharField(max_length=16)

    def __str__(self):
        return u"{0}".format(self.type)


class Video(AuditableModel):
    file = models.FileField(null=True, blank=True)


class Annotator(models.Model):
    # todo:  the volunteer anotators will need logins, etc.  tie back to auth.User?
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    affiliation = models.CharField(max_length=100)

    def __str__(self):
        return u"{0}, {1}".format(self.last_name, self.first_name)


class VideoAnnotator(AuditableModel):
    annotator = models.ForeignKey(to=Annotator)
    video = models.ForeignKey(to=Video)
    assigned_by = models.ForeignKey(to=User, related_name='assigned_by')


class Observation(AuditableModel):
    initial_observation_time = models.DateTimeField()

    animal = models.ForeignKey(Animal)
    sex = models.CharField(max_length=1,
                           choices=ANIMAL_SEX_CHOICES, default='U')
    stage = models.CharField(max_length=2,
                             choices=ANIMAL_STAGE_CHOICES, default='U')
    length = models.IntegerField(null=True, help_text='centimeters')

    behavior = models.ForeignKey(to=AnimalBehavior, null=True)
    duration = models.PositiveIntegerField()

    set = models.ForeignKey('bruv.Set')
    video_annotator = models.ForeignKey(VideoAnnotator)

    def __str__(self):
        return u"{0}".format(self.initial_observation_time)


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
    set = models.ForeignKey('bruv.Set')

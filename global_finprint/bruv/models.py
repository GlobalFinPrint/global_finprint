from django.contrib.gis.db import models
from django.core.urlresolvers import reverse

from global_finprint.core.models import AuditableModel
from global_finprint.trip.models import Trip, Reef
from global_finprint.habitat.models import Benthic


class Observer(models.Model):
    # todo:  placeholder for "tape reader"  create a real name list.
    name = models.CharField(max_length=100, unique=True)


class Animal(models.Model):
    common_name = models.CharField(max_length=100)
    family = models.CharField(max_length=100, unique=True)
    genus = models.CharField(max_length=100, unique=True)
    species = models.CharField(max_length=100, unique=True)
    fishbase_key = models.IntegerField(null=True)
    sealifebase_key = models.IntegerField(null=True)

    def __str__(self):
        return u"{0} {1} ({2})".format(self.genus, self.species, self.common_name)


FISH_SEX_CHOICES = {
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Unknown'),
}
FISH_STAGE_CHOICES = {
    ('AD', 'Adult'),
    ('JU', 'Juvenile'),
    ('U', 'Unknown'),
}


class ObservedAnimal(models.Model):
    animal = models.ForeignKey(Animal)
    sex = models.CharField(max_length=1, choices=FISH_SEX_CHOICES)
    stage = models.TextField(max_length=2, choices=FISH_STAGE_CHOICES)

    # length in cm
    length = models.IntegerField(null=True, help_text='centimeters')

    # todo:  ... controlled vocabularies?
    activity = models.TextField(max_length=25, null=True)
    behavior = models.TextField(max_length=50, null=True)


class Equipment(AuditableModel):
    # todo:  should be a controlled list
    camera = models.CharField(max_length=100)
    stereo = models.BooleanField(default=False)
    # todo:  should be a controlled list ... get pictures, etc.
    bruv_frame = models.CharField(max_length=100)

    def __str__(self):
        return u"{0}: {1}".format(self.bruv_frame, self.camera)


class Set(AuditableModel):
    location = models.PointField(null=True)
    drop_time = models.DateTimeField()
    collection_time = models.DateTimeField(null=True, blank=True)
    time_bait_gone = models.DateTimeField(null=True, blank=True)

    equipment = models.ForeignKey(Equipment)
    depth = models.FloatField(null=True)
    # todo:  should be a controlled list
    bait = models.CharField(max_length=100)

    reef = models.ForeignKey(Reef, null=True)
    trip = models.ForeignKey(Trip)

    def get_absolute_url(self):
        return reverse('set_update', args=[str(self.id)])

    def __str__(self):
        return u"{0}".format(self.drop_time)


class EnvironmentMeasure(AuditableModel):
    measurement_time = models.DateTimeField()
    water_tmperature = models.FloatField(null=True)
    salinity = models.FloatField(null=True)
    conductivity = models.FloatField(null=True)
    dissolved_oxygen = models.FloatField(null=True)
    current_flow = models.FloatField(null=True)

    set = models.ForeignKey(Set)


class Observation(AuditableModel):
    initial_observation_time = models.DateTimeField()
    observed_fish = models.ForeignKey(ObservedAnimal)

    maximum_number_observed = models.IntegerField(null=True)
    maximum_number_observed_time = models.DateTimeField(null=True)

    set = models.ForeignKey(Set)
    observer = models.ForeignKey(Observer)


class Video(AuditableModel):
    # todo:  placeholder!  this should be filesystem / S3 ...
    name = models.FileField()
    length = models.FloatField()
    set = models.ForeignKey(Set)


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
    set = models.ForeignKey(Set)

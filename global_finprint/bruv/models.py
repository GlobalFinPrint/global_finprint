from django.contrib.gis.db import models

from global_finprint.core.models import AuditableModel
from global_finprint.trip.models import Trip, Reef
from global_finprint.habitat.models import Benthic


class Observer(models.Model):
    # todo:  placeholder for "tape reader"  create a real name list.
    name = models.CharField(max_length=100, unique=True)


class Fish(models.Model):
    family = models.CharField(max_length=100, unique=True)
    genus = models.CharField(max_length=100, unique=True)
    species = models.CharField(max_length=100, unique=True)
    fishbase_key = models.IntegerField()


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


class ObservedFish(models.Model):
    fish = models.ForeignKey(Fish)
    sex = models.CharField(max_length=1, choices=FISH_SEX_CHOICES)
    stage = models.TextField(max_length=2, choices=FISH_STAGE_CHOICES)
    # todo:  controlled lists
    size = models.TextField(max_length=10, null=True)
    activity = models.TextField(max_length=10, null=True)
    behavior = models.TextField(max_length=50, null=True)
    # todo:  ...


class Equipment(AuditableModel):
    # todo:  should be a controlled list
    camera = models.CharField(max_length=100)
    stereo = models.BooleanField(default=False)
    # todo:  should be a controlled list ... get pictures, etc.
    bruv_frame = models.CharField(max_length=100)
    # todo:  should be a controlled list
    bait = models.CharField(max_length=100)


class Set(AuditableModel):
    location = models.PointField()
    drop_time = models.DateTimeField()
    collection_time = models.DateTimeField(null=True)
    time_bait_gone = models.DateTimeField(null=True)

    equipment = models.ForeignKey(Equipment)
    depth = models.FloatField(null=True)
    #benthic = models.ForeignKey(Benthic, null=True, default=None)

    reef = models.ForeignKey(Reef, null=True)
    trip = models.ForeignKey(Trip)

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
    observed_fish = models.ForeignKey(ObservedFish)

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

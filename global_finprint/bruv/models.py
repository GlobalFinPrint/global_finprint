from django.contrib.gis.db import models

from global_finprint.cruise.models import Cruise
from global_finprint.benthos.models import BenthicCategory


class Equipment(models.Model):
    # todo:  placeholder!
    name = models.CharField(max_length=100, unique=True)
    # todo:  should be a controlled list
    camera = models.CharField(max_length=100, unique=True)


class Video(models.Model):
    # todo:  placeholder!
    name = models.CharField(max_length=100, unique=True)


class Fish(models.Model):
    family = models.CharField(max_length=100, unique=True)
    genus = models.CharField(max_length=100, unique=True)
    species = models.CharField(max_length=100, unique=True)
    # todo:  external ids?  e.g., FishBase key, CAAB code?


class Site(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.PointField()
    benthic_category = models.ForeignKey(BenthicCategory)
    description = models.CharField(max_length=4000, null=True, blank=True)

    cruises = models.ManyToManyField(Cruise, through='Deployment')

    objects = models.GeoManager()

    def __str__(self):
        return u"{0}".format(self.name)


class Deployment(models.Model):
    drop_time = models.DateTimeField()
    collection_time = models.DateTimeField()
    time_bait_gone = models.DateTimeField()

    equipment = models.ForeignKey(Equipment)
    depth = models.FloatField()

    video = models.ForeignKey(Video)
    site = models.ForeignKey(Site)
    cruise = models.ForeignKey(Cruise)


class EnvironmentMeasure(models.Model):
    measurement_time = models.DateTimeField()
    water_tmperature = models.FloatField()
    salinity = models.FloatField()
    conductivity = models.FloatField()
    dissolved_oxygen = models.FloatField()
    current_flow = models.FloatField()

    deployment = models.ForeignKey(Deployment)


class Observation(models.Model):
    measurement_time = models.DateTimeField()
    water_tmperature = models.FloatField()
    salinity = models.FloatField()
    conductivity = models.FloatField()
    dissolved_oxygen = models.FloatField()
    current_flow = models.FloatField()
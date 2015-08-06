from django.contrib.gis.db import models

from global_finprint.core.models import AuditableModel


class Location(models.Model):
    name = models.CharField(max_length=100)
    boundary = models.MultiPolygonField(srid=4326)

    objects = models.GeoManager()

    def __str__(self):
        return u"{0}".format(self.name)


class Site(models.Model):
    location = models.ForeignKey(Location)
    name = models.CharField(max_length=100)
    boundary = models.MultiPolygonField(srid=4326)

    objects = models.GeoManager()

    def __str__(self):
        return u"{0}".format(self.name)


class Reef(models.Model):
    site = models.ForeignKey(Site)
    name = models.CharField(max_length=100)
    boundary = models.MultiPolygonField(srid=4326)

    objects = models.GeoManager()

    def __str__(self):
        return u"{0}".format(self.name)


class Trip(AuditableModel):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location)
    boat = models.CharField(max_length=200)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    type = models.CharField(max_length=200)

    objects = models.GeoManager()

    def __str__(self):
        return u"{0} - {1}".format(self.boat, self.name)







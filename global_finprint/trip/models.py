from django.contrib.gis.db import models

from global_finprint.core.models import AuditableModel


class Location(models.Model):
    name = models.CharField(max_length=100)
    boundary = models.MultiPolygonField(srid=4326, null=True)

    objects = models.GeoManager()

    def __str__(self):
        return u"{0}".format(self.name)


class Site(models.Model):
    location = models.ForeignKey(Location)
    name = models.CharField(max_length=100)
    boundary = models.MultiPolygonField(srid=4326, null=True)

    objects = models.GeoManager()

    def __str__(self):
        return u"{0}".format(self.name)


class Reef(models.Model):
    site = models.ForeignKey(Site)
    name = models.CharField(max_length=100, null=True)
    # todo:  assign a contorlled vocabulary (e.g., forereef, reef flat, pass,
    #   lagoon, inner slope, etc.)
    type = models.CharField(max_length=100)
    boundary = models.MultiPolygonField(srid=4326, null=True)

    objects = models.GeoManager()

    def __str__(self):
        return u"{0}".format(self.name)


class Team(AuditableModel):
    # todo:  or group, etc.  maybe useful for controlling data access during restricted periods?
    association = models.CharField(max_length=100)
    # todo:  person's name.  add to controlled list
    lead = models.CharField(max_length=100)
    # todo:  some other people ...
    def __str__(self):
        return u"{0}-{1}".format(self.association, self.lead)


class Trip(AuditableModel):
    # todo:  what is the expectaion of name?
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team)
    location = models.ForeignKey(Location)
    boat = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    # todo:  what is this for?
    type = models.CharField(max_length=100)

    def __str__(self):
        # todo:  whatever is most usefully readable ...
        return u"{0} ({2} - {3})".format(self.team,
                                         self.start_datetime.date().isoformat(),
                                         self.end_datetime.date().isoformat()
                                         )

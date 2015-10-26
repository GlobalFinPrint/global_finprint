from django.contrib.gis.db import models

from global_finprint.core.models import AuditableModel


class Location(models.Model):
    name = models.CharField(max_length=100)

    objects = models.GeoManager()

    def __str__(self):
        return u"{0}".format(self.name)


class Site(models.Model):
    location = models.ForeignKey(Location)
    name = models.CharField(max_length=100)
    boundary = models.MultiPolygonField(srid=4326, null=True)
    # todo type:
    #     continental, island, atoll

    objects = models.GeoManager()

    def __str__(self):
        return u"{0}".format(self.name)


class Reef(models.Model):
    site = models.ForeignKey(Site)
    name = models.CharField(max_length=100, null=True)

    # todo:  assign a contorlled vocabulary (e.g., slope, crest, flat, back reef, lagoon)
    type = models.CharField(max_length=100)
    boundary = models.MultiPolygonField(srid=4326, null=True)

    # todo:  protection status [1]
    #     openly fished, restricted, unfished, remote
    # todo:  dominant gear in use (shark fishing) [0/1]
    #     gillnet, spear, longline, seine, rod and reel, poly ball / highflyer, drumline
    # todo:  restrictions [0-oo]
    #     gear, species, effort, size
    # todo:  MPA size km^2
    # todo:  MPA age
    # todo:  MPA compliance  (see Edgar)
    #     low ("paper park"), medium ("some poaching"), high (well enforced)
    # todo:  MPA physical isolation  (see Edgar)
    #     continuous, <20m to next reef, >20m to next reef

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
    team = models.ForeignKey(Team)
    location = models.ForeignKey(Location)
    boat = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    # todo:  what is this for?
    type = models.CharField(max_length=100)

    def __str__(self):
        # todo:  whatever is most usefully readable ...
        return u"{0} ({1} - {2})".format(self.team,
                                         self.start_date.isoformat(),
                                         self.end_date.isoformat()
                                         )

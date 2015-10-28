from django.contrib.gis.db import models

from global_finprint.core.models import AuditableModel


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return u"{0}".format(self.name)


class Location(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(to=Region)

    def __str__(self):
        return u"{0}".format(self.name)


SITE_TYPE_CHOICES = {
    ('C', 'Continental'),
    ('I', 'Island'),
    ('A', 'Atoll'),
}


class Site(models.Model):
    location = models.ForeignKey(Location)
    name = models.CharField(max_length=100)
    boundary = models.MultiPolygonField(srid=4326, null=True)
    type = models.CharField(max_length=16, choices=SITE_TYPE_CHOICES)

    objects = models.GeoManager()

    def __str__(self):
        return u"{0}".format(self.name)


class MPACompliance(models.Model):
    """
        see Edgar, G., et al.  Nature 506, 216-220 (13 Feb 2014)
        doi:10.1038/nature13022
        values:  low ("paper park"), medium ("some poaching"), high (well enforced)
    """
    type = models.CharField(max_length=16)
    description = models.CharField(max_length=24)

    def __str__(self):
            return u"{0} ({1})".format(self.type, self.description)

    class Meta:
        verbose_name = "MPA compliance"
        verbose_name_plural = "MPA compliance"


class MPAIsolation(models.Model):
    """
        see Edgar, G., et al.  Nature 506, 216-220 (13 Feb 2014)
        doi:10.1038/nature13022
        values:  continuous, <20m to next reef, >20m to next reef
    """
    type = models.CharField(max_length=24)

    def __str__(self):
            return u"{0}".format(self.type)

    class Meta:
        verbose_name = "MPA isolation"
        verbose_name_plural = "MPA isolation"


class MPA(models.Model):
    name = models.CharField(max_length=100)
    boundary = models.MultiPolygonField(srid=4326, null=True)
    # todo:  create property that takes area from polygon first then area field if no poly
    area = models.PositiveIntegerField(help_text='km^2')
    founded = models.PositiveIntegerField()

    mpa_compliance = models.ForeignKey(to=MPACompliance)
    mpa_isolation = models.ForeignKey(to=MPAIsolation)

    objects = models.GeoManager()

    def __str__(self):
        return u"{0}".format(self.name)

    class Meta:
        verbose_name = "MPA"
        verbose_name_plural = "MPAs"


class ReefType(models.Model):
    """
        part of reef
        values:  slope, crest, flat, back reef, lagoon
    """
    type = models.CharField(max_length=16)

    def __str__(self):
            return u"{0}".format(self.type)


class ProtectionStatus(models.Model):
    """
        protection status is a required attribute of a reef
        values:  openly fished, restricted, unfished, remote
    """
    type = models.CharField(max_length=16)

    def __str__(self):
            return u"{0}".format(self.type)

    class Meta:
        verbose_name_plural = "Protection status"


class SharkGearInUse(models.Model):
    """
        dominant gear in use for shark fishing
        values:  gillnet, spear, longline, seine, rod and reel, poly ball / highflyer, drumline
    """
    type = models.CharField(max_length=24)

    def __str__(self):
            return u"{0}".format(self.type)

    class Meta:
        verbose_name_plural = "Shark gear in use"


class FishingRestrictions(models.Model):
    """
        restrictions on shark fishing gear
        values:  gear, species, effort, size
    """
    type = models.CharField(max_length=16)

    def __str__(self):
            return u"{0}".format(self.type)

    class Meta:
        verbose_name_plural = "Fishing restrictions"


class Reef(models.Model):
    site = models.ForeignKey(Site)
    name = models.CharField(max_length=100)

    boundary = models.MultiPolygonField(srid=4326, null=True)

    type = models.ForeignKey(to=ReefType)
    protection_status = models.ForeignKey(to=ProtectionStatus)
    shark_gear_in_use = models.ForeignKey(to=SharkGearInUse, null=True)
    # todo:  restrictions [0-oo]

    mpa = models.ForeignKey(to=MPA, null=True)

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

    def __str__(self):
        # todo:  whatever is most usefully readable ...
        return u"{0} ({1} - {2})".format(self.team,
                                         self.start_date.isoformat(),
                                         self.end_date.isoformat()
                                         )

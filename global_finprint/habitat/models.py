from decimal import Decimal

from django.contrib.gis.db import models
from django.core.validators import MinValueValidator

from ..core.models import Team


class Substrate(models.Model):
    type = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return u"{0}".format(self.type)


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return u"{0}".format(self.name)


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=4, unique=True, help_text='3166-1 alpha-2, if applicable.')
    boundary = models.MultiPolygonField(srid=4326, null=True, blank=True)
    eez_boundary = models.MultiPolygonField(srid=4326, null=True, blank=True)

    region = models.ForeignKey(to=Region)

    @property
    def reef_set(self):
        return Reef.objects.filter(site__in=self.site_set.all().values_list('id', flat=True))

    def __str__(self):
        return u"{0} ({1})".format(self.name, self.code)


SITE_TYPE_CHOICES = {
    ('C', 'Continental'),
    ('I', 'Island'),
    ('A', 'Atoll'),
}


class Site(models.Model):
    name = models.CharField(max_length=100, help_text='Must be unique for site location.')
    code = models.CharField(max_length=4, help_text='Must be unique for site location.')
    location = models.ForeignKey(Location)
    boundary = models.MultiPolygonField(srid=4326, null=True, blank=True)
    type = models.CharField(max_length=1, choices=SITE_TYPE_CHOICES)

    planned_team = models.ForeignKey(to=Team, null=True)

    objects = models.GeoManager()

    def __str__(self):
        return u"{0} - {1} ({2})".format(self.location, self.name, self.code)

    class Meta:
        unique_together = (('location', 'name'),
                           ('location', 'code'),)


class MPACompliance(models.Model):
    """
        see Edgar, G., et al.  Nature 506, 216-220 (13 Feb 2014)
        doi:10.1038/nature13022
        values:  low ("paper park"), medium ("some poaching"), high (well enforced)
    """
    type = models.CharField(max_length=16)
    description = models.CharField(max_length=48)

    def __str__(self):
        return u"{0}{1}".format(self.type,
                                ' (' + self.description + ')' if self.description and len(self.description) > 0 else '')

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
    boundary = models.MultiPolygonField(srid=4326, null=True, blank=True)
    # todo:  create property that takes area from polygon first then area field if no poly
    area = models.DecimalField(help_text='km^2', null=True, blank=True, decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))])
    founded = models.PositiveIntegerField(null=True, blank=True)

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
    code = models.CharField(max_length=1)
    description = models.CharField(max_length=48)

    def __str__(self):
            return u"{0}".format(self.type)

    class Meta:
        verbose_name = "Reef habitat"


class ProtectionStatus(models.Model):
    """
        protection status is a required attribute of a reef
        values:  openly fished, restricted, unfished, remote
    """
    type = models.CharField(max_length=16)
    description = models.CharField(max_length=48)

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
    description = models.CharField(max_length=48)

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
    description = models.CharField(max_length=48)

    def __str__(self):
            return u"{0}".format(self.type)

    class Meta:
        verbose_name_plural = "Fishing restrictions"


class Reef(models.Model):
    name = models.CharField(max_length=100, help_text='Must be unique for reef site.')
    code = models.CharField(max_length=5, help_text='Must be unique for reef site.')
    site = models.ForeignKey(Site)

    boundary = models.MultiPolygonField(srid=4326, null=True, blank=True)

    protection_status = models.ForeignKey(to=ProtectionStatus)
    shark_gear_in_use = models.ManyToManyField(to=SharkGearInUse, blank=True)
    fishing_restrictions = models.ManyToManyField(to=FishingRestrictions, blank=True)

    mpa = models.ForeignKey(to=MPA, null=True, blank=True)

    old_manager = models.Manager()
    objects = models.GeoManager()

    def __str__(self):
        return u"{0} - {1} ({2}{3})".format(self.site.name, self.name, self.site.code, self.code)

    class Meta:
        unique_together = (('site', 'name'),
                           ('site', 'code'),)


class ReefHabitat(models.Model):
    reef = models.ForeignKey(Reef)
    habitat = models.ForeignKey(ReefType)

    @classmethod
    def get_or_create(cls, reef, habitat):
        try:
            return cls.objects.get(reef=reef, habitat=habitat)
        except cls.DoesNotExist:
            new_reef_habitat = cls(reef=reef, habitat=habitat)
            new_reef_habitat.save()
            return new_reef_habitat

    def __str__(self):
        return u"{0} - {1} ({2})".format(self.reef.site, self.reef.name, self.habitat.type)

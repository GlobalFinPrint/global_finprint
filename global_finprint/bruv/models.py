from django.contrib.gis.db import models
from django.core.urlresolvers import reverse

from global_finprint.core.models import AuditableModel
from global_finprint.trip.models import Trip, Reef
# from global_finprint.habitat.models import Benthic


class Observer(models.Model):
    # todo:  placeholder for "tape reader"  create a real name list.
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return u"{0}".format(self.name)


class Animal(models.Model):
    common_name = models.CharField(max_length=100)
    family = models.CharField(max_length=100, unique=True)
    genus = models.CharField(max_length=100, unique=True)
    species = models.CharField(max_length=100, unique=True)
    fishbase_key = models.IntegerField(null=True)
    sealifebase_key = models.IntegerField(null=True)

    def __str__(self):
        return u"{0} {1} ({2})".format(self.genus, self.species, self.common_name)


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


# class ObservedAnimal(models.Model):
#     animal = models.ForeignKey(Animal)
#     sex = models.CharField(max_length=1, choices=ANIMAL_SEX_CHOICES)
#     stage = models.TextField(max_length=2, choices=ANIMAL_STAGE_CHOICES)
#
#     # length in cm
#     length = models.IntegerField(null=True, help_text='centimeters')
#
#     # todo:  ... controlled vocabularies?
#     activity = models.TextField(max_length=25, null=True)
#     behavior = models.TextField(max_length=50, null=True)
#
# ANIMAL_STAGE_CHOICES = {
#     ('AD', 'Adult'),
#     ('JU', 'Juvenile'),
#     ('U', 'Unknown'),
# }

class Equipment(AuditableModel):
    # todo:  should be a controlled list
    camera = models.CharField(max_length=100)
    stereo = models.BooleanField(default=False)
    # todo:  bag, cage

    # todo:  should be a controlled list
    #      rebar, stainless rebar, PVC, mixed
    frame_type = models.CharField(max_length=100)

    # todo:  arm_length
    # todo:  camera_height


    def __str__(self):
        return u"{0}: {1}".format(self.bruv_frame, self.camera)


class Set(AuditableModel):
    # location used elsewhere ...
    coordinates = models.PointField(null=True)
    drop_time = models.DateTimeField()
    collection_time = models.DateTimeField(null=True, blank=True)

    # time_bait_gone = models.DateTimeField(null=True, blank=True)

    # todo:  tide_state

    # todo:  visibility (meters 1,2,3 ... 15, >15) if different from daily

    equipment = models.ForeignKey(Equipment)

    depth = models.FloatField(null=True)
    # todo:  should be a controlled list ... add +- menhedden oil, add 1kg / 20ml
    bait = models.CharField(max_length=100)

    reef = models.ForeignKey(Reef, null=True)
    trip = models.ForeignKey(Trip)

    def get_absolute_url(self):
        return reverse('set_update', args=[str(self.id)])

    def __str__(self):
        return u"{0}".format(self.drop_time)


class EnvironmentMeasure(AuditableModel):
    measurement_time = models.DateTimeField()
    water_temperature = models.IntegerField(null=True)  # C
    salinity = models.FloatField(null=True)  # ppt .0
    conductivity = models.FloatField(null=True)  # S/m .00
    dissolved_oxygen = models.FloatField(null=True)  # % .0
    current_flow = models.FloatField(null=True)  # m/s .00
    current_direction = models.FloatField(null=True)  # eight point compass

    set = models.ForeignKey(Set)


class Observation(AuditableModel):
    initial_observation_time = models.DateTimeField()

    # observed_animal = models.ForeignKey(ObservedAnimal)
    animal = models.ForeignKey(Animal)
    sex = models.CharField(max_length=1, choices=ANIMAL_SEX_CHOICES, default='U')
    stage = models.CharField(max_length=2, choices=ANIMAL_STAGE_CHOICES, default='U')

    # length in cm
    length = models.IntegerField(null=True, help_text='centimeters')

    # todo:  ... controlled vocabularies?
    #    swim by, stimulated, interaction
    behavior = models.CharField(max_length=50, null=True, blank=True)

    # maximum_number_observed = models.IntegerField(null=True)
    # maximum_number_observed_time = models.DateTimeField(null=True)

    # todo:  duration in seconds

    set = models.ForeignKey(Set)
    observer = models.ForeignKey(Observer)

    def __str__(self):
        return u"{0}".format(self.initial_observation_time)


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

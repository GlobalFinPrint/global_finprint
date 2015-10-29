from django.contrib.gis.db import models
from django.core.urlresolvers import reverse

from global_finprint.core.models import AuditableModel
from global_finprint.trip.models import Trip, Reef


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
EQUIPMENT_BAIT_CONTAINER = {
    ('B', 'Bag'),
    ('C', 'Cage'),
}
CURRENT_DIRECTION = {
    ('N', 'North'),
    ('NE', 'Northeast'),
    ('E', 'East'),
    ('SE', 'Southeast'),
    ('S', 'South'),
    ('SW', 'Southwest'),
    ('W', 'West'),
    ('NW', 'Northwest'),
}
VISIBILITY_CHOICES = {
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('>15', '>15'),
}

class FrameType(models.Model):
    # rebar, stainless rebar, PVC, mixed
    type = models.CharField(max_length=16)
    image = models.ImageField(null=True)

    def __str__(self):
        return u"{0}".format(self.type)


class Equipment(AuditableModel):
    camera = models.CharField(max_length=16)
    stereo = models.BooleanField(default=False)
    frame_type = models.ForeignKey(to=FrameType)
    bait_container = models.CharField(max_length=1, choices=EQUIPMENT_BAIT_CONTAINER, default='C')
    arm_length = models.PositiveIntegerField(help_text='centimeters')
    camera_height = models.PositiveIntegerField(help_text='centimeters')

    def __str__(self):
        return u"{0} / {1}".format(self.frame_type.type, self.camera)

    class Meta:
        verbose_name_plural = "Equipment"


class Set(AuditableModel):
    coordinates = models.PointField(null=True)
    drop_time = models.DateTimeField()
    collection_time = models.DateTimeField(null=True, blank=True)

    # todo:  tide_state values?
    tide_state = models.CharField(max_length=16)
    visibility = models.CharField(max_length=3, choices=VISIBILITY_CHOICES)

    equipment = models.ForeignKey(Equipment)

    depth = models.FloatField(null=True)
    bait = models.CharField(max_length=16, help_text='1kg')
    bait_oiled = models.BooleanField(default=False, help_text='20ml menhaden oil')

    reef = models.ForeignKey(Reef, null=True)
    trip = models.ForeignKey(Trip)

    def get_absolute_url(self):
        return reverse('set_update', args=[str(self.id)])

    def __str__(self):
        return u"{0}".format(self.drop_time)


class EnvironmentMeasure(AuditableModel):
    measurement_time = models.DateTimeField()
    water_temperature = models.IntegerField(null=True,
                                            help_text='C')  # C
    salinity = models.DecimalField(null=True,
                                   max_digits=4, decimal_places=2,
                                   help_text='ppt')  # ppt .0
    conductivity = models.DecimalField(null=True,
                                       max_digits=4, decimal_places=2,
                                       help_text='S/m')  # S/m .00
    dissolved_oxygen = models.DecimalField(null=True,
                                           max_digits=3, decimal_places=1,
                                           help_text='%')  # % .0
    current_flow = models.DecimalField(null=True,
                                       max_digits=5, decimal_places=2,
                                       help_text='m/s')  # m/s .00
    current_direction = models.CharField(max_length=2,
                                         null=True,
                                         choices=CURRENT_DIRECTION,
                                         help_text='compass direction')  # eight point compass
    set = models.ForeignKey(Set)


class AnimalBehavior(models.Model):
    #    swim by, stimulated, interaction
    type = models.CharField(max_length=16)

    def __str__(self):
        return u"{0}".format(self.type)


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

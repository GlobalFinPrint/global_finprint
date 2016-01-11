from django.contrib.gis.db import models
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Point

from global_finprint.core.models import AuditableModel
from global_finprint.trip.models import Trip
from global_finprint.habitat.models import ReefHabitat


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
TIDE_CHOICES = {
    ('F', 'Flood'),
    ('E', 'Ebb'),
    ('S', 'Slack'),
    ('S2F', 'Slack to Flood'),
    ('S2E', 'Slack to Ebb'),
}
SURFACE_CHOP_CHOICES = {
    ('L', 'Light'),
    ('M', 'Medium'),
    ('H', 'Heavy'),
}
BAIT_TYPE_CHOICES = {
    ('CHP', 'Chopped'),
    ('CRS', 'Crushed'),
    ('WHL', 'Whole'),
}


class FrameType(models.Model):
    # starting seed:  rebar, stainless rebar, PVC, mixed
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


class EnvironmentMeasure(AuditableModel):
    water_temperature = models.DecimalField(null=True, blank=True,
                                            max_digits=4, decimal_places=1,
                                            help_text='C')  # C
    salinity = models.DecimalField(null=True, blank=True,
                                   max_digits=4, decimal_places=2,
                                   help_text='ppt')  # ppt .0
    conductivity = models.DecimalField(null=True, blank=True,
                                       max_digits=4, decimal_places=2,
                                       help_text='S/m')  # S/m .00
    dissolved_oxygen = models.DecimalField(null=True, blank=True,
                                           max_digits=3, decimal_places=1,
                                           help_text='%')  # % .0
    current_flow = models.DecimalField(null=True, blank=True,
                                       max_digits=5, decimal_places=2,
                                       help_text='m/s')  # m/s .00
    current_direction = models.CharField(max_length=2,
                                         null=True, blank=True,
                                         choices=CURRENT_DIRECTION,
                                         help_text='compass direction')  # eight point compass
    tide_state = models.CharField(max_length=3,
                                  null=True, blank=True,
                                  choices=TIDE_CHOICES)
    estimated_wind_speed = models.IntegerField(null=True, blank=True)
    wind_direction = models.CharField(max_length=2,
                                      null=True, blank=True,
                                      choices=CURRENT_DIRECTION,
                                      help_text='compass direction')  # eight point compass
    cloud_cover = models.IntegerField(null=True, blank=True, help_text='%')  # percentage
    surface_chop = models.CharField(max_length=1,
                                    null=True, blank=True,
                                    choices=SURFACE_CHOP_CHOICES)

    def __str__(self):
        return u'{0}'.format(self.measurement_time)


class Bait(AuditableModel):
    description = models.CharField(max_length=16, help_text='1kg')
    type = models.CharField(max_length=3, choices=BAIT_TYPE_CHOICES)
    oiled = models.BooleanField(default=False, help_text='20ml menhaden oil')


class Set(AuditableModel):
    code = models.CharField(max_length=32)
    # drop_id = models.CharField(max_length=32)
    set_date = models.DateField()
    coordinates = models.PointField(null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    drop_time = models.TimeField()
    haul_time = models.TimeField()
    visibility = models.CharField(max_length=3, choices=VISIBILITY_CHOICES)
    depth = models.FloatField(null=True, help_text='m')
    comments = models.CharField(max_length=255, null=True, blank=True)

    equipment = models.ForeignKey(Equipment)
    reef_habitat = models.ForeignKey(ReefHabitat)
    trip = models.ForeignKey(Trip)

    bait = models.OneToOneField(
        Bait,
        on_delete=models.CASCADE,
        null=True,
        related_name='bait_parent_set')
    drop_measure = models.OneToOneField(
        EnvironmentMeasure,
        on_delete=models.CASCADE,
        null=True,
        related_name='drop_parent_set')
    haul_measure = models.OneToOneField(
        EnvironmentMeasure,
        on_delete=models.CASCADE,
        null=True,
        related_name='haul_parent_set')
    video = models.OneToOneField(
        'annotation.Video',
        on_delete=models.CASCADE,
        null=True,
        related_name='set'
    )

    @property
    def environmentmeasure_set(self):
        return [x for x in [self.haul_measure, self.drop_measure] if x is not None]

    def save(self, *args, **kwargs):
        # todo:  we're assuming the input is latitude & longitude!  this should be checked!
        self.coordinates = Point(float(self.longitude), float(self.latitude))
        super(Set, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('set_update', args=[str(self.id)])

    def __str__(self):
        return u"{0}".format(self.code)

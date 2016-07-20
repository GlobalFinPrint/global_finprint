from decimal import Decimal

from django.contrib.gis.db import models
from django.core.validators import MinValueValidator
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Point

from global_finprint.annotation.models.observation import Observation
from global_finprint.annotation.models.video import Video
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
    ('0', 'LEGACY'),
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
    image = models.ImageField(null=True, blank=True)

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
    estimated_wind_speed = models.IntegerField(null=True, blank=True, help_text='Beaufort')
    wind_direction = models.CharField(max_length=2,
                                      null=True, blank=True,
                                      choices=CURRENT_DIRECTION,
                                      help_text='compass direction')  # eight point compass
    cloud_cover = models.IntegerField(null=True, blank=True, help_text='%')  # percentage
    surface_chop = models.CharField(max_length=1,
                                    null=True, blank=True,
                                    choices=SURFACE_CHOP_CHOICES)

    def __str__(self):
        return u'{0} {1}'.format('Env measure for',str(self.set))


class Bait(AuditableModel):
    description = models.CharField(max_length=16, help_text='1kg')
    type = models.CharField(max_length=3, choices=BAIT_TYPE_CHOICES)
    oiled = models.BooleanField(default=False, help_text='20ml menhaden oil')

    def __str__(self):
        return u'{0} {1} {2}'.format(self.get_type_display(), self.description, '*' if self.oiled else '')

    class Meta:
        unique_together = ('description', 'type', 'oiled')


class Set(AuditableModel):
    # suggested code pattern:
    # [site.code][reef.code]_[set number within reef]
    code = models.CharField(max_length=32, help_text='[site + reef code]_xxx', null=True, blank=True)
    set_date = models.DateField()
    coordinates = models.PointField(null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    drop_time = models.TimeField()
    haul_time = models.TimeField()
    visibility = models.CharField(max_length=3, choices=VISIBILITY_CHOICES)
    depth = models.DecimalField(null=True, help_text='m', decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.01'))])
    comments = models.TextField(null=True, blank=True)

    # todo:  need some form changes here ...
    bait = models.ForeignKey(Bait, null=True)
    equipment = models.ForeignKey(Equipment)
    reef_habitat = models.ForeignKey(ReefHabitat, blank=True)
    trip = models.ForeignKey(Trip)

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
        Video,
        on_delete=models.CASCADE,
        null=True,
        related_name='set'
    )

    class Meta:
        unique_together = ('trip', 'code')

    @property
    def environmentmeasure_set(self):
        return [x for x in [self.haul_measure, self.drop_measure] if x is not None]

    def save(self, *args, **kwargs):
        # todo:  we're assuming the input is latitude & longitude!  this should be checked!
        self.coordinates = Point(float(self.longitude), float(self.latitude))
        if not self.code:  # set code if it hasn't been set
            self.code = u'{}{}_xxx'.format(self.reef().site.code, self.reef().code)
        super(Set, self).save(*args, **kwargs)
        self.refresh_from_db()
        if self.code == u'{}{}_xxx'.format(self.reef().site.code, self.reef().code):
            next_id = str(len(Set.objects.filter(trip=self.trip, reef_habitat__reef=self.reef()))).zfill(3)
            self.code = self.code.replace('_xxx', u'_{}'.format(next_id))
            super(Set, self).save(*args, **kwargs)

    def reef(self):
        return self.reef_habitat.reef

    def get_absolute_url(self):
        return reverse('set_update', args=[str(self.id)])

    def observations(self):
        return Observation.objects.filter(assignment__in=self.video.assignment_set.all())

    def __str__(self):
        return u"{0}_{1}".format(self.trip.code, self.code)

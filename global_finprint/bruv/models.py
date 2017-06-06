from decimal import Decimal
from collections import Counter

from django.contrib.gis.db import models
from django.core.validators import MinValueValidator
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Point

from global_finprint.annotation.models.observation import Observation, MasterRecord
from global_finprint.annotation.models.video import Video, Assignment
from global_finprint.core.version import VersionInfo
from global_finprint.core.models import AuditableModel
from global_finprint.trip.models import Trip
from global_finprint.habitat.models import ReefHabitat, Substrate, SubstrateComplexity

from mptt.models import MPTTModel, TreeForeignKey

# todo:  move some of these out ot the db?
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
    type = models.CharField(max_length=32)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return u"{0}".format(self.type)


class Equipment(AuditableModel):
    camera = models.CharField(max_length=32)
    stereo = models.BooleanField(default=False)
    frame_type = models.ForeignKey(to=FrameType)
    bait_container = models.CharField(max_length=1, choices=EQUIPMENT_BAIT_CONTAINER, default='C')
    arm_length = models.PositiveIntegerField(null=True, help_text='centimeters')
    camera_height = models.PositiveIntegerField(null=True, help_text='centimeters')

    def __str__(self):
        return u"{0} / {1}{2}".format(self.frame_type.type, self.camera, ' (Stereo)' if self.stereo else '')

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
                                       max_digits=8, decimal_places=2,
                                       help_text='S/m')  # S/m .00
    dissolved_oxygen = models.DecimalField(null=True, blank=True,
                                           max_digits=8, decimal_places=1)
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
    measured_wind_speed = models.IntegerField(null=True, blank=True, help_text='kts')
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
    description = models.CharField(max_length=32, help_text='1kg')
    type = models.CharField(max_length=3, choices=BAIT_TYPE_CHOICES)
    oiled = models.BooleanField(default=False, help_text='20ml menhaden oil')

    def __str__(self):
        return u'{0} {1}{2}'.format(self.get_type_display(), self.description, ' (m)' if self.oiled else '')

    class Meta:
        unique_together = ('description', 'type', 'oiled')


# needed for SetTag#get_choices because python doesn't have this somehow (!!!)
def flatten(x):
    if type(x) is list:
        return [a for i in x for a in flatten(i)]
    else:
        return [x]


class SetTag(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(
        default=True,
        help_text='overridden if parent is inactive')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return u"{0}".format(self.name)

    @classmethod
    def get_choices(cls, node=None):
        if node is None:
            nodes = [cls.get_choices(node=node) for node in cls.objects.filter(parent=None, active=True)]
            return [(node.pk, node.name) for node in flatten(nodes)]
        elif node.is_leaf_node():
            return node
        else:
            return [node] + [cls.get_choices(node=node) for node in node.get_children().filter(active=True)]


class BenthicCategory(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(
        default=True,
        help_text='overridden if parent is inactive')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return u"{0}".format(self.name)

    class Meta:
        verbose_name_plural = 'benthic categories'


class Set(AuditableModel):
    # suggested code pattern:
    # [site.code][reef.code]_[set number within reef]
    code = models.CharField(max_length=32, help_text='[site + reef code]_xxx', null=True, blank=True)
    set_date = models.DateField()
    coordinates = models.PointField(null=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    drop_time = models.TimeField()
    haul_date = models.DateField(null=True, blank=True)
    haul_time = models.TimeField(null=True, blank=True)
    visibility = models.CharField(max_length=3, choices=VISIBILITY_CHOICES, help_text='m')
    depth = models.DecimalField(help_text='m', decimal_places=2, max_digits=12,
                                validators=[MinValueValidator(Decimal('0.01'))])
    comments = models.TextField(null=True, blank=True)
    message_to_annotators = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(to=SetTag)
    current_flow_estimated = models.CharField(max_length=50, null=True, blank=True, help_text='H, M, L')
    current_flow_instrumented = models.DecimalField(null=True, blank=True,
                                                    max_digits=5, decimal_places=2,
                                                    help_text='m/s')  # m/s .00
    bruv_image_url = models.CharField(max_length=200, null=True, blank=True)
    splendor_image_url = models.CharField(max_length=200, null=True, blank=True)

    benthic_category = models.ManyToManyField(BenthicCategory, through='BenthicCategoryValue')
    substrate = models.ForeignKey(Substrate, blank=True, null=True)
    substrate_complexity = models.ForeignKey(SubstrateComplexity, blank=True, null=True)

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
        if self.video:
            return Observation.objects.filter(assignment__in=self.video.assignment_set.all())

    def habitat_filename(self, image_type):
        server_env = VersionInfo.get_server_env()
        return '/{0}/{1}/{2}/{3}.png'.format(server_env,
                                             self.trip.code,
                                             self.code,
                                             image_type)

    # todo:  "property-ize" this?
    def master(self, project=1):
        try:
            return MasterRecord.objects.get(set=self, project_id=project)
        except MasterRecord.DoesNotExist:
            return None

    def assignment_counts(self, project=1):
        status_list = {'Total': 0}
        if self.video:
            status_list.update(Counter(Assignment.objects.filter(
                video=self.video, project=project).values_list('status__id', flat=True)))
            status_list['Total'] = sum(status_list.values())
        return status_list

    def required_fields(self):
        # need to make this data-driven, not hard-coded field choices
        # currently required:
        # 1) visibility
        # 2) current flow (either)
        # 3) substrate
        # 4) substrate complexity
        return bool(self.visibility
                    and (self.current_flow_estimated or self.current_flow_instrumented)
                    and self.substrate and self.substrate_complexity)

    def completed(self):
        # we consider the following for "completion":
        # 1) complete annotations have been promoted into a master
        # 2) a master annotation record has been completed
        # 3) other 'required' fields have been completed (see above)
        master = self.master()
        return master \
               and (master.status.is_finished) \
               and self.required_fields()

    def __str__(self):
        return u"{0}_{1}".format(self.trip.code, self.code)


class BenthicCategoryValue(models.Model):
    set = models.ForeignKey(Set)
    benthic_category = TreeForeignKey(BenthicCategory)
    value = models.IntegerField()

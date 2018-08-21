from django.db import connection
from django.contrib.gis.db import models

from ..annotation.models.video import Video, Assignment
from ..annotation.models.animal import Animal
from ..annotation.models.observation import Observation, Event
from ..core.models import Team, FinprintUser
from ..habitat.models import Region, Location, Site, Reef, ReefHabitat
from ..trip.models import Trip
from ..bruv.models import Set
import logging

REPORT_PREFIX = 'v_report_'


class Report:
    def __init__(self, db_view):
        self.db_view = db_view if REPORT_PREFIX in db_view else '{}{}'.format(REPORT_PREFIX, db_view)

    @classmethod
    def view_list(cls):
        """ Excluded Reports """
        excluded_reports = {
            "1": "annotation_status_by_annotator",
            "2": "annotation_status_by_team",
            "3": "assignment_status",
            "4": "assignment_status_by_file",
            "6": "global_set_counts",
            "7": "global_set_counts_by_source",
            "8": "machine_learning_corpus_from_assignment",
            "11": "maxn_issues_report",
            "15": "observations_coral_summary",
            "17": "observations_io_summary",
            "20": "observations_pac_summary",
            "22": "observations_wa_summary",
            "25": "reef_summary",
            "26": "set_counts_by_location",
            "28": "sets_without_video",
            "29": "sitelist_summary",
            "30": "species_observation_counts",
            "31": "usage_metrics",
            "32": "usage_metrics_by_affiliation",
            "33": "weekly_video_hours",
            "34": "zero_time_assignment_images",
            "35": "zero_time_images"
        }

        with connection.cursor() as cursor:
            query = "SELECT table_name FROM INFORMATION_SCHEMA.views " \
                    "WHERE table_name LIKE '{}%%'" \
                    "ORDER BY table_name".format(REPORT_PREFIX)
            cursor.execute(query)
            returned_list = []
            excluded_list = []
            for row in cursor.fetchall():
                if str(cls(row[0])) in excluded_reports.values():
                    excluded_list.append(cls(row[0]))
                else:
                    returned_list.append(cls(row[0]))
            return returned_list

    def results(self, limit=None):
        if not limit:
            limit = 'all'
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM {} limit {}".format(self.db_view, limit))
            return [tuple(col[0] for col in cursor.description)] + cursor.fetchall()

    def __str__(self):
        return u'{}'.format(self.db_view.replace(REPORT_PREFIX, ''))


# summary views for reporting
class EventAttributeSummary(models.Model):
    set_code = models.CharField(max_length=32)
    trip = models.ForeignKey(Trip, on_delete=models.DO_NOTHING)
    set = models.ForeignKey(Set, on_delete=models.DO_NOTHING)
    reef_habitat = models.ForeignKey(ReefHabitat, on_delete=models.DO_NOTHING)

    video = models.ForeignKey(Video, on_delete=models.DO_NOTHING)
    assignment = models.ForeignKey(Assignment, on_delete=models.DO_NOTHING)
    annotator = models.ForeignKey(FinprintUser, on_delete=models.DO_NOTHING)

    observation = models.ForeignKey(Observation, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    animal = models.ForeignKey(Animal, on_delete=models.DO_NOTHING)

    event_time = models.IntegerField(help_text='ms', default=0)

    zero_time_em_note = models.BooleanField()
    haul_time_em_note = models.BooleanField()
    zero_time_tagged = models.BooleanField()
    sixty_minute_time_tagged = models.BooleanField()
    ninty_minute_time_tagged = models.BooleanField()
    haul_time_tagged = models.BooleanField()
    max_n_tagged = models.BooleanField()

    numeric_value_from_event_note = models.IntegerField()
    numeric_value_from_obs_comment = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'event_attribute_summary'


# a sql view that can be used for the geo hierarchy
class HabitatSummary(models.Model):
    reef_habitat_id = models.IntegerField(primary_key=True)
    region_name = models.TextField()
    location_name = models.TextField()
    site_name = models.TextField()
    reef_name = models.TextField()
    reef_habitat_name = models.TextField()

    site_type = models.TextField()
    reef_protected_status = models.TextField()
    mpa_name = models.TextField()
    mpa_compliance = models.TextField()
    mpa_isolation = models.TextField()

    region_id = models.IntegerField()
    location_id = models.IntegerField()
    site_id = models.IntegerField()
    reef_id = models.IntegerField()
    mpa_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'habitat_summary'

    @classmethod
    def get_for_api(cls):
        return list(ob.to_json() for ob in cls.objects.all())

    def to_json(self):
        return {
            'reef_habitat_id': self.reef_habitat_id,
            'region_name': self.region_name,
            'location_name': self.location_name,
            'site_name': self.site_name,
            'reef_name': self.reef_name,
            'reef_habitat_name': self.reef_habitat_name,

            'site_type': self.site_type,
            'reef_protected_status': self.reef_protected_status,
            'mpa_name': self.mpa_name,
            'mpa_compliance': self.mpa_compliance,
            'mpa_isolation': self.mpa_isolation,

            'region_id': self.region_id,
            'location_id': self.location_id,
            'site_id': self.site_id,
            'reef_id': self.reef_id,
            'mpa_id': self.mpa_id,
        }


class ObservationSummary(models.Model):
    summary_id = models.IntegerField(primary_key=True)
    trip_code = models.TextField()
    set_code = models.TextField()
    full_code = models.TextField()
    region_name = models.TextField()
    location_name = models.TextField()
    site_name = models.TextField()
    reef_name = models.TextField()
    reef_habitat_name = models.TextField()
    animal_id = models.IntegerField()
    family = models.TextField()
    genus = models.TextField()
    species = models.TextField()
    maxn = models.IntegerField()
    event_time_minutes_raw = models.TextField()
    event_time_minutes = models.TextField()
    trip_id = models.IntegerField()
    set_id = models.IntegerField()
    video_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'observation_summary'

    @classmethod
    def get_for_api(cls, region):
        if region:
            return list(ob.to_json() for ob in cls.objects.filter(region_name__iexact=region))
        else:
            return list(ob.to_json() for ob in cls.objects.all())

    def to_json(self):
        return {
            'summary_id': self.summary_id,
            'trip_code': self.trip_code,
            'set_code': self.set_code,
            'full_code': self.full_code,
            'region_name': self.region_name,
            'location_name': self.location_name,
            'site_name': self.site_name,
            'reef_name': self.reef_name,
            'reef_habitat_name': self.reef_habitat_name,
            'family': self.family,
            'genus': self.genus,
            'species': self.species,
            'event_time_minutes_raw': self.event_time_minutes_raw,
            'event_time_minutes': self.event_time_minutes,
            'maxn': self.maxn,
            'trip_id': self.trip_id,
            'set_id': self.set_id,
            'video_id': self.video_id,
        }


class SetSummary(models.Model):
    set_id = models.IntegerField(primary_key=True)
    team = models.TextField()
    trip_code = models.TextField()
    set_code = models.TextField()
    region_name = models.TextField()
    location_name = models.TextField()
    site_name = models.TextField()
    reef_name = models.TextField()
    reef_habitat_name = models.TextField()
    reef_habitat_id = models.IntegerField()
    set_date = models.DateField()
    drop_time = models.TimeField()
    haul_time = models.TimeField()

    wkt_coordinates = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

    depth = models.DecimalField(max_digits=6, decimal_places=2)

    equipment_frame_type = models.TextField()
    equipment_camera = models.TextField()
    equipment_stereo_camera = models.BooleanField()
    equipment_camera_height = models.TextField()
    equipment_arm_length = models.TextField()

    bait_preparation = models.TextField()
    bait_type = models.TextField()
    bait_oiled = models.BooleanField()

    visibility = models.TextField()

    current_flow_estimated = models.TextField()
    current_flow_instrumented = models.DecimalField(max_digits=6, decimal_places=2)

    substrate_type = models.TextField()
    substrate_complexity_type = models.TextField()
    bruv_image_url = models.TextField()
    splendor_image_url = models.TextField()

    video_file_name = models.TextField()
    video_source = models.TextField()
    video_path = models.TextField()

    class Meta:
        managed = False
        db_table = 'set_summary'

    @classmethod
    def get_for_api(cls, region):
        if region:
            return list(ob.to_json() for ob in cls.objects.filter(region_name__iexact=region))
        else:
            return list(ob.to_json() for ob in cls.objects.filter())

    def to_json(self):
        return {
            'set_id': self.set_id,
            'team': self.team,
            'trip_code': self.trip_code,
            'set_code': self.set_code,
            'region_name': self.region_name,
            'location_name': self.location_name,
            'site_name': self.site_name,
            'reef_name': self.reef_name,
            'reef_habitat_name': self.reef_habitat_name,
            'reef_habitat_id': self.reef_habitat_id,
            'set_date': self.set_date,
            'drop_time': self.drop_time,
            'haul_time': self.haul_time,

            'wkt_coordinates': self.wkt_coordinates,
            'latitude': self.latitude,
            'longitude': self.longitude,

            'depth': self.depth,
            'visibility': self.visibility,

            'equipment': {

                'frame_type': self.equipment_frame_type,
                'camera': self.equipment_camera,
                'stereo': self.equipment_stereo_camera,
                'camera_height': self.equipment_camera_height,
                'arm_length': self.equipment_arm_length,
            },
            'bait': {
                'preparation': self.bait_preparation,
                'type': self.bait_type,
                'oiled': self.bait_oiled,
            },

            'current_flow_estimated': self.current_flow_estimated,
            'current_flow_instrumented': self.current_flow_instrumented,
            'substrate_type': self.substrate_type,
            'substrate_complexity_type': self.substrate_complexity_type,
            'bruv_image_url': self.bruv_image_url,
            'reef_image_url': self.splendor_image_url,

            'video' : {
                'file_name': self.video_file_name,
                'source': self.video_source,
                'path': self.video_path,
            },
        }


# leaderboards
class MonthlyLeaderboard(models.Model):
    leaderboard_id = models.IntegerField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    affiliation_name = models.TextField()
    month = models.TextField()
    num_assignments = models.IntegerField()
    hours = models.DecimalField(max_digits=12, decimal_places=2)
    affiliation_count_rank = models.IntegerField()
    affiliation_hour_rank = models.IntegerField()

    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'monthly_leaderboard'



# todo: not currently used ... intended for status mapping.
PLANNED_TRIP_STATUS_CHOICES = {
    ('W', 'Wishlist'),
    ('F', 'Forthcoming'),
    ('P', 'In Progress'),
    ('C', 'Completed'),
}


class PlannedSiteStatus(models.Model):
    planned_start_date = models.DateField(null=True)
    planned_end_date = models.DateField(null=True)
    funder = models.TextField(null=True)
    status = models.CharField(max_length=1, choices=PLANNED_TRIP_STATUS_CHOICES)
    name = models.TextField(null=True)
    eez_boundary = models.MultiPolygonField(null=True)
    site_id = models.IntegerField(null=True)
    team_id = models.IntegerField(null=True)

    objects = models.GeoManager()

    class Meta:
        managed = False


class PlannedSite(models.Model):
    location = models.ForeignKey(to=Location)
    site = models.ForeignKey(to=Site, null=True)
    planned_start_date = models.DateField(null=True, blank=True)
    planned_end_date = models.DateField(null=True, blank=True)

    funder = models.TextField(null=True, blank=True)
    team = models.ForeignKey(to=Team, null=True)
    trip = models.ManyToManyField(to=Trip)

    status = models.CharField(max_length=1, choices=PLANNED_TRIP_STATUS_CHOICES)

    def __str__(self):
        return u"{0} ({1} - {2})".format(self.location.name, self.team.name, self.planned_date)

from django.db import connection
from django.contrib.gis.db import models

from ..annotation.models.video import Video, Assignment
from ..annotation.models.animal import Animal
from ..annotation.models.observation import Observation, Event
from ..core.models import Team, FinprintUser
from ..habitat.models import Location, Site, Reef, ReefHabitat
from ..trip.models import Trip
from ..bruv.models import Set

REPORT_PREFIX = 'v_report_'


class Report:
    def __init__(self, db_view):
        self.db_view = db_view if REPORT_PREFIX in db_view else '{}{}'.format(REPORT_PREFIX, db_view)

    @classmethod
    def view_list(cls):
        with connection.cursor() as cursor:
            query = "SELECT table_name FROM INFORMATION_SCHEMA.views " \
                    "WHERE table_name LIKE '{}%%'" \
                    "ORDER BY table_name".format(REPORT_PREFIX)
            cursor.execute(query)
            return list(cls(row[0]) for row in cursor.fetchall())

    def results(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM {}".format(self.db_view))
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


class HabitatSummary(models.Model):
    region = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    site = models.CharField(max_length=100)
    reef = models.CharField(max_length=100)
    reef_habitat_name = models.CharField(max_length=100)
    reef_habitat = models.ForeignKey(ReefHabitat, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'habitat_summary'


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

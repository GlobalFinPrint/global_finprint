from django.db import connection
from django.contrib.gis.db import models

from ..core.models import Team
from ..habitat.models import Location, Site
from ..trip.models import Trip


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


PLANNED_TRIP_STATUS_CHOICES = {
    ('W', 'Wishlist'),
    ('F', 'Forthcoming'),
    ('P', 'In Progress'),
    ('C', 'Completed'),
}

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


class Planned_Site_Status(models.Model):
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

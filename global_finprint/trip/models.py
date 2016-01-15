from django.contrib.gis.db import models

from global_finprint.core.models import AuditableModel
from global_finprint.habitat.models import Location


class Team(AuditableModel):
    # todo:  or group, etc.  maybe useful for controlling data access during restricted periods?
    association = models.CharField(max_length=100)
    # todo:  person's name.  add to controlled list
    lead = models.CharField(max_length=100)
    # todo:  some other people ...

    def __str__(self):
        return u"{0} - {1}".format(self.association, self.lead)


class Trip(AuditableModel):
    # suggested code pattern:
    # FP_[location.code]_[start_date.year]_[trip number within location / year]
    code = models.CharField(max_length=32, help_text='FP_[year]_[loc code]_xx')  # todo:  unique??
    team = models.ForeignKey(Team)
    location = models.ForeignKey(Location)
    boat = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def region(self):
        return self.location.region

    def __str__(self):
        return u"{0}".format(self.code)

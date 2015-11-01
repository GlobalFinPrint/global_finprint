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
    team = models.ForeignKey(Team)
    location = models.ForeignKey(Location)
    boat = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        # todo:  whatever is most usefully readable ...
        #   feedback: need this to be searchable: year, location ... team may be less useful.
        return u"{0} ({1} - {2})".format(self.location.name,
                                         self.start_date.isoformat(),
                                         self.end_date.isoformat()
                                         )

from django.contrib.gis.db import models

from global_finprint.core.models import AuditableModel
from global_finprint.habitat.models import Location
from global_finprint.annotation.models import Lead


class Team(AuditableModel):
    sampler_collaborator = models.CharField(max_length=100)
    lead = models.ForeignKey(to=Lead, related_name='POC')

    class Meta:
        unique_together = ('lead', 'sampler_collaborator')

    def __str__(self):
        return u"{0} - {1}".format(self.sampler_collaborator, self.lead.user.username)


class Trip(AuditableModel):
    # suggested code pattern:
    # FP_[location.code]_[start_date.year]_[trip number within location / year]
    code = models.CharField(max_length=32, help_text='FP_[year]_[loc code]_xx', null=True, blank=True)  # todo:  unique??
    team = models.ForeignKey(Team)
    location = models.ForeignKey(Location)
    boat = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.code:  # trip code if it hasn't been set:  FP_[year]_[loc code]_xx
            self.code = u'FP_{}_{}_xx'.format(self.start_date.year, self.location.code)
        super(Trip, self).save(*args, **kwargs)
        self.refresh_from_db()
        next_id = str(len(Trip.objects.filter(location=self.location)) + 1).zfill(2)
        self.code = self.code.replace('_xx', u'_{}'.format(next_id))
        super(Trip, self).save(*args, **kwargs)

    @property
    def region(self):
        return self.location.region

    def __str__(self):
        return u"{0}".format(self.code)

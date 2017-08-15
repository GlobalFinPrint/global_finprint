from datetime import datetime, timedelta

from django.contrib.gis.db import models

from global_finprint.core.models import AuditableModel, Team
from global_finprint.habitat.models import Location


class Source(models.Model):
    name = models.CharField(max_length=32)
    data_embargo_length = models.PositiveIntegerField(null=True, default=9999, help_text='Days to embargo data after trip ends. 9999 = "embargo forever"')
    code = models.CharField(max_length=3, unique=True)
    legacy = models.BooleanField(default=False)

    def __str__(self):
        return u"{0}".format(self.name)


class Trip(AuditableModel):
    # suggested code pattern:
    # [source]_[start_date.year]_[location.code]_[trip number within location / year]
    code = models.CharField(max_length=32, db_index=True, help_text='[source code]_[year]_[loc code]_xx', unique=True, null=True, blank=True)
    team = models.ForeignKey(Team)
    location = models.ForeignKey(Location)
    boat = models.CharField(max_length=32, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    source = models.ForeignKey(to=Source, null=True)
    data_embargo_termination = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:  # trip code if it hasn't been set:  [source]_[year]_[loc code]_xx
            self.code = u'{}_{}_{}_xx'.format(self.source.code, self.start_date.year, self.location.code)
        if not self.data_embargo_termination:
            if self.source.data_embargo_length >= 9999:
                self.data_embargo_termination = datetime.max
            else:
                self.data_embargo_termination = self.end_date + timedelta(days=self.source.data_embargo_length)
        super(Trip, self).save(*args, **kwargs)
        self.refresh_from_db()
        if self.code == u'{}_{}_{}_xx'.format(self.source.code, self.start_date.year, self.location.code):
            next_id = str(len(Trip.objects.filter(location=self.location, start_date__year=self.start_date.year))).zfill(2)
            self.code = self.code.replace('_xx', u'_{}'.format(next_id))
            super(Trip, self).save(*args, **kwargs)

    @property
    def region(self):
        return self.location.region

    def completed(self):
        return all(s.completed() for s in self.set_set.all())

    def __str__(self):
        return u"{0}".format(self.code)

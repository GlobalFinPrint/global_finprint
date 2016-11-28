from django.apps import apps
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from config.current_user import get_current_user
import uuid


class TimestampedModel(models.Model):
    create_datetime = models.DateTimeField(auto_now_add=True)
    last_modified_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditableModel(TimestampedModel):
    user = models.ForeignKey(to=User, default=get_current_user)

    class Meta:
        abstract = True


class Affiliation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return u"{0}".format(self.name)

    def annotators(self):
        return self.finprintuser_set.all()

    class Meta:
        ordering = ['name']


class FinprintUser(models.Model):
    user = models.OneToOneField(to=User)
    affiliation = models.ForeignKey(to=Affiliation)
    token = models.CharField(max_length=32, null=True, blank=True)

    @classmethod
    def get_leads(cls):
        return cls.objects.filter(user__groups__id=1)

    def set_token(self):
        self.token = uuid.uuid4().hex
        self.save()
        return self.token

    def clear_token(self):
        self.token = None
        self.save()
        return True

    def active_assignments(self):
        return apps.get_model('annotation', 'Assignment').objects.filter(annotator=self, status__in=[1, 2, 5]).all()

    def is_lead(self):
        return self.user.groups.filter(id=1).exists()

    def is_superuser(self):
        return self.user.is_superuser

    def __str__(self):
        return u"{0}, {1} ({2})".format(self.user.last_name, self.user.first_name, self.affiliation.name)

    def to_json(self):
        return {
            'id': self.id,
            'name': "{0}, {1}".format(self.user.last_name, self.user.first_name),
            'affiliation': self.affiliation.name,
            'assignments': [{'id': a.id, 'set': a.set().code, 'status': str(a.status)}
                            for a in self.assignment_set.all()],
            'observations': [{'id': o.id, 'time': o.initial_observation_time()}
                             for o in self.observations_created.all()]
        }


class Team(AuditableModel):
    sampler_collaborator = models.CharField(max_length=100)
    lead = models.ForeignKey(to=FinprintUser, related_name='POC')

    class Meta:
        unique_together = ('lead', 'sampler_collaborator')

    def __str__(self):
        return u"{0}{1}{2}".format(self.lead.user.username, (' - ' if self.sampler_collaborator else ''), self.sampler_collaborator)

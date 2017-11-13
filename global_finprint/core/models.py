import datetime
from django.apps import apps
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from config.current_user import get_current_user
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.serializers.json import DjangoJSONEncoder
import uuid


class TimestampedModel(models.Model):
    create_datetime = models.DateTimeField(auto_now_add=True)
    last_modified_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditableModel(TimestampedModel):
    # user and last_modified_by are nullable to enable data migration (get_current_user returns None)
    user = models.ForeignKey(to=User, default=get_current_user, null=True)
    last_modified_by = models.ForeignKey(to=User, default=get_current_user, null=True,
                                         related_name='%(app_label)s_%(class)s_last_modified_by')

    def save(self, *args, **kwargs):
        self.last_modified_by = get_current_user()
        super(AuditableModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class VersionedModel(AuditableModel):
    def to_json(self):
        return {}

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.add_version()
        super(VersionedModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.add_version(True)
        super(VersionedModel, self).save(*args, **kwargs)

    def add_version(self, deleted=False):
        class_name = '.'.join([self.__module__, self.__class__.__name__])
        history, _ = ModelHistory.objects.get_or_create(model_type=class_name, reference_id=self.pk)
        if deleted:
            history.deleted = True
        my_json = self.serialize_datetimes(self.to_json())
        user = self.last_modified_by or self.user
        snapshot = ModelSnapshot(create_datetime=self.last_modified_datetime,
                                 user=user,
                                 state=my_json,
                                 history=history)
        snapshot.save()

    # The below code can be removed in django 1.11, and django.core.serializers.json.DjangoJSONEncoder
    # can instead be passed to the JSONField definition using the new "encoder" keyword parameter.
    @staticmethod
    def serialize_datetimes(obj):
        if isinstance(obj, dict):
            result = {}
            for key, item in obj.items():
                result[key] = VersionedModel.serialize_datetimes(item)
            return result
        elif isinstance(obj, list) or isinstance(obj, tuple):
            result = []
            for item in obj:
                result.append(VersionedModel.serialize_datetimes(item))
            return result
        elif isinstance(obj, datetime.datetime):
            return str(obj)
        else:
            return obj


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

    @staticmethod
    def get_lead_users():
        return User.objects.filter(groups__id=1)

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

    def clear_active_assignments(self):
        active_assignments = self.active_assignments()
        for assignment in active_assignments:
            assignment.remove()

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

    class Meta:
        ordering = ['user__last_name', 'user__first_name']


class Team(AuditableModel):
    sampler_collaborator = models.CharField(max_length=100)
    lead = models.ForeignKey(to=FinprintUser, related_name='POC')

    class Meta:
        unique_together = ('lead', 'sampler_collaborator')

    def __str__(self):
        return u"{0}{1}{2}".format(self.lead.user.username, (' - ' if self.sampler_collaborator else ''), self.sampler_collaborator)

class ModelHistory(models.Model):
    model_type = models.TextField()
    reference_id = models.IntegerField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return u'pk: {0}, type: {1}, ref_id: {2}'.format(self.pk, self.model_type, self.reference_id)

class ModelSnapshot(models.Model):
    create_datetime = models.DateTimeField()
    user = models.ForeignKey(to=User)
    state = JSONField()
    history = models.ForeignKey(to=ModelHistory)

    def __str__(self):
        return u'pk: {0}, user: {1}, date: {2}, history_ref: {3}'.format(
            self.pk, str(self.user), str(self.create_datetime), self.history.pk)

    class Meta():
        ordering = ['create_datetime']


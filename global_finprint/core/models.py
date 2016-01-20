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


class FinprintUser(models.Model):
    user = models.OneToOneField(to=User)
    affiliation = models.ForeignKey(to=Affiliation)
    token = models.CharField(max_length=32, null=True)

    def set_token(self):
        self.token = uuid.uuid4().hex
        self.save()
        return self.token

    def clear_token(self):
        self.token = None
        self.save()
        return True

    def __str__(self):
        return u"{0}, {1} ({2})".format(self.user.last_name, self.user.first_name, self.affiliation.name)

    class Meta:
        abstract = True

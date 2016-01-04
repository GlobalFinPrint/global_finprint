from django.contrib.gis.db import models
from django.contrib.auth.models import User
from config.current_user import get_current_user


class TimestampedModel(models.Model):
    create_datetime = models.DateTimeField(auto_now_add=True)
    last_modified_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuditableModel(TimestampedModel):
    user = models.ForeignKey(to=User, default=get_current_user)

    class Meta:
        abstract = True


class FinprintUser(models.Model):
    user = models.ForeignKey(to=User)
    affiliation = models.CharField(max_length=100)

    def __str__(self):
        return u"{0}, {1} ({2})".format(self.user.last_name, self.user.first_name, self.affiliation)

    class Meta:
        abstract = True

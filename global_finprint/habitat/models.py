from django.contrib.gis.db import models

from global_finprint.core.models import AuditableModel


class Substrate(models.Model):
    type = models.CharField(max_length=24, unique=True)

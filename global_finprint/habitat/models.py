from django.contrib.gis.db import models

from global_finprint.core.models import AuditableModel


class Substrate(models.Model):
    # todo:  see Google doc for values ... this is deployment data
    name = models.CharField(max_length=100, unique=True)

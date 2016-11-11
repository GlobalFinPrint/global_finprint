from django.db import models
from global_finprint.core.models import AuditableModel
from .animal import Animal


class Project(AuditableModel):
    name = models.CharField(max_length=100)
    description = models.TextField(default=True, blank=True)
    animals = models.ManyToManyField(Animal)

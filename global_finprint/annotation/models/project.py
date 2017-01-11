from django.db import models
from global_finprint.core.models import AuditableModel
from .animal import Animal, AnimalGroup


class Project(AuditableModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    animals = models.ManyToManyField(Animal)

    def __str__(self):
        return u'{0}'.format(self.name)

    def animal_groups(self):
        group_ids = self.animals.all().distinct('group').values_list('group__id')
        return AnimalGroup.objects.filter(id__in=group_ids)

from django.db import models
from global_finprint.core.models import AuditableModel
from django.apps import apps


class Project(AuditableModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return u'{0}'.format(self.name)

    # def animal_groups(self):
    #     group_ids = self.animals.all().distinct('group').values_list('group__id')
    #     return AnimalGroup.objects.filter(id__in=group_ids)

    def tag_list(self):
        inactive_ids = set()
        for a in apps.get_model('annotation', 'Attribute').objects.filter(active=False):
            inactive_ids = (inactive_ids | set(a.id for a in a.get_descendants(include_self=True)))
        return self.attribute_set.filter(not_selectable=False).exclude(id__in=inactive_ids)

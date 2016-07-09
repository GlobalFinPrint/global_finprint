from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Attribute(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(
        default=True,
        help_text='overridden if parent is inactive')
    lead_only = models.BooleanField(
        default=False,
        help_text='overridden if parent is lead only')

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return u"{0}".format(self.name)

    def to_json(self, children=True, is_lead=True):
        json = {
            'id': self.pk,
            'name': self.name,
            'description': self.description,
            'level': self.get_level()
        }
        if children and not self.is_leaf_node():
            children = list(a for a in self.get_children() if a.active)
            if not is_lead:
                children = list(a for a in children if not a.lead_only)
            json['children'] = list(a.to_json(children=True, is_lead=is_lead) for a in children)
        return json

    @staticmethod
    def tree_json(is_lead=True):
        root_nodes = list(a for a in Attribute.objects.root_nodes() if a.active)
        if not is_lead:
            root_nodes = list(a for a in root_nodes if not a.lead_only)
        return list(a.to_json(children=True, is_lead=is_lead) for a in root_nodes)

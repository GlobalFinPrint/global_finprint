from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Attribute(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return u"{0}".format(self.name)

    def to_json(self, children=False):
        json = {
            'id': self.pk,
            'name': self.name,
            'description': self.description,
        }
        if children and not self.is_leaf_node():
            json['children'] = list(a.to_json() for a in self.get_children())
        return json

    @classmethod
    def tree_json(cls):
        return list(a.to_json(children=True) for a in Attribute.objects.root_nodes())

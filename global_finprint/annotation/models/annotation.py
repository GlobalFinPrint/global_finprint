from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .project import Project


class GlobalAttribute(MPTTModel):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'GlobalTag'

    def __str__(self):
        return u"{0}".format(self.name)


class Attribute(MPTTModel):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(
        default=True,
        help_text='overridden if parent is inactive')
    lead_only = models.BooleanField(
        default=False,
        help_text='overridden if parent is lead only')
    needs_review = models.BooleanField(default=False)
    not_selectable = models.BooleanField(default=False)
    global_parent = models.ForeignKey(to=GlobalAttribute, null=True, blank=True)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    project = models.ForeignKey(Project, default=1)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Tag'
        unique_together = (('name', 'project'),)

    def __str__(self):
        return u"{0}".format(self.name)

    def verbose_name(self):
        return '/'.join(list(map(str, self.get_ancestors(include_self=True))))

    def to_json(self, children=True, is_lead=True):
        json = {
            'id': self.pk,
            'name': self.name,
            'verbose': self.verbose_name(),
            'description': self.description,
            'level': self.get_level(),
            'not_selectable': self.not_selectable,
            'global_parent_id': self.global_parent_id if self.global_parent_id else -1 #sending -1 if global_parent_id is null
        }
        if children and not self.is_leaf_node():
            children = list(a for a in self.get_children() if a.active)
            if not is_lead:
                children = list(a for a in children if not a.lead_only)
            json['children'] = list(a.to_json(children=True, is_lead=is_lead) for a in children)
        return json

    @staticmethod
    def tree_json(is_lead=True, project=None):
        root_nodes = list(a for a in Attribute.objects.root_nodes()
                          if a.active and (a.project == project or project is None))
        if not is_lead:
            root_nodes = list(a for a in root_nodes if not a.lead_only)
        return list(a.to_json(children=True, is_lead=is_lead) for a in root_nodes)

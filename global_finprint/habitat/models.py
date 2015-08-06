from django.contrib.gis.db import models

from global_finprint.core.models import AuditableModel


class Category(models.Model):
    # todo:  placeholder
    name = models.CharField(max_length=100, unique=True)


class Form(models.Model):
    # todo:  placeholder
    name = models.CharField(max_length=100, unique=True)


class Community(models.Model):
    # todo:  placeholder
    name = models.CharField(max_length=100, unique=True)


class Substrate(models.Model):
    # todo:  placeholder
    name = models.CharField(max_length=100, unique=True)


class Benthic(AuditableModel):
    # todo:  placeholder
    substrate = models.ForeignKey(to=Substrate)
    category = models.ForeignKey(to=Category, null=True)
    community = models.ForeignKey(to=Community, null=True)
    form = models.ForeignKey(to=Form, null=True)
    comment = models.TextField(max_length=500, null=True)





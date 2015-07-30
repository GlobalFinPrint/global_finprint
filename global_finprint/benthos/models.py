from django.contrib.gis.db import models


class BenthicCategory(models.Model):
    # todo:  placeholder
    name = models.CharField(max_length=100, unique=True)


class BenthicCommunity(models.Model):
    # todo:  placeholder
    name = models.CharField(max_length=100, unique=True)


class Substrate(models.Model):
    # todo:  placeholder
    name = models.CharField(max_length=100, unique=True)


class Benthic(models.Model):
    # todo:  placeholder
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(to=BenthicCategory)
    community = models.ForeignKey(to=BenthicCommunity)
    substrate = models.ForeignKey(to=Substrate)






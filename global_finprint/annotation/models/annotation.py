from django.db import models


class AnimalBehavior(models.Model):
    #    swim by, stimulated, interaction
    type = models.CharField(max_length=16)

    def __str__(self):
        return u"{0}".format(self.type)


class ObservationFeature(models.Model):
    id = models.AutoField(primary_key=True)
    feature = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return u"{0}".format(self.feature)

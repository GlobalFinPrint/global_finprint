from django.contrib.gis.db import models


class Cruise(models.Model):
    boat = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    type = models.CharField(max_length=200)

    objects = models.GeoManager()

    def __str__(self):
        return u"{0} - {1}".format(self.boat, self.name)







from django.contrib import admin

from global_finprint.bruv import models

# Register your models here.
admin.site.register(models.Set)
admin.site.register(models.Observer)
admin.site.register(models.Observation)
admin.site.register(models.EnvironmentMeasure)
admin.site.register(models.Equipment)
admin.site.register(models.Animal)
admin.site.register(models.ObservedAnimal)


from django.contrib import admin

from global_finprint.bruv import models


admin.site.register(models.Observer)
admin.site.register(models.FrameType)
admin.site.register(models.Equipment)
admin.site.register(models.AnimalBehavior)
admin.site.register(models.Animal)


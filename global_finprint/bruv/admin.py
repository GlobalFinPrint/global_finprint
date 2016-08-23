from django.contrib import admin

from global_finprint.bruv import models


admin.site.register(models.Bait)
admin.site.register(models.FrameType)
admin.site.register(models.Equipment)
admin.site.register(models.SetTag)
admin.site.register(models.Substrate)

from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from global_finprint.trip import models


admin.site.register(models.Region, LeafletGeoAdmin)
admin.site.register(models.Location, LeafletGeoAdmin)
admin.site.register(models.MPACompliance)
admin.site.register(models.MPAIsolation)
admin.site.register(models.MPA)
admin.site.register(models.ReefType)
admin.site.register(models.ProtectionStatus)
admin.site.register(models.SharkGearInUse)
admin.site.register(models.Reef, LeafletGeoAdmin)
admin.site.register(models.FishingRestrictions)
admin.site.register(models.Team)
admin.site.register(models.Site, LeafletGeoAdmin)
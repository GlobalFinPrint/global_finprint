from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from global_finprint.habitat import models



class LocationAdmin(LeafletGeoAdmin):
    ordering = ['name']
    search_fields = ['name']


class SiteAdmin(LeafletGeoAdmin):
    list_filter = ['location__name']
    ordering = ['location__name', 'name']
    search_fields = ['location__name', 'name']


class ReefAdmin(LeafletGeoAdmin):
    list_filter = ['site__location__name', 'site__name']
    ordering = ['site__name', 'name']
    search_fields = ['site__location__name', 'site__name', 'name']


class MPAAdmin(LeafletGeoAdmin):
    ordering = ['name']
    search_fields = ['name']


admin.site.register(models.Region, LeafletGeoAdmin)
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Site, SiteAdmin)
admin.site.register(models.Reef, ReefAdmin)
admin.site.register(models.MPA, MPAAdmin)

admin.site.register(models.Substrate)
admin.site.register(models.MPACompliance)
admin.site.register(models.MPAIsolation)
admin.site.register(models.ReefType)
admin.site.register(models.ProtectionStatus)
admin.site.register(models.SharkGearInUse)
admin.site.register(models.FishingRestrictions)

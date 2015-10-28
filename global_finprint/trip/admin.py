from django.contrib import admin

from global_finprint.trip.models import Region, Location, Team, Site, \
    MPACompliance, MPAIsolation, MPA, \
    ReefType, ProtectionStatus, SharkGearInUse, FishingRestrictions, Reef


admin.site.register(Region)
admin.site.register(Location)
admin.site.register(MPACompliance)
admin.site.register(MPAIsolation)
admin.site.register(MPA)
admin.site.register(ReefType)
admin.site.register(ProtectionStatus)
admin.site.register(SharkGearInUse)
admin.site.register(Reef)
admin.site.register(FishingRestrictions)
admin.site.register(Team)
admin.site.register(Site)
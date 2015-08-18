from django.contrib import admin

# Register your models here.
from global_finprint.trip.models import Trip, Location, Reef, Team

admin.site.register(Trip)
admin.site.register(Location)
admin.site.register(Reef)
admin.site.register(Team)
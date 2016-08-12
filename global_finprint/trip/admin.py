from django.contrib import admin
from global_finprint.trip import models


class SiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'data_embargo_length', 'code', 'legacy']

admin.site.register(models.Source, SiteAdmin)

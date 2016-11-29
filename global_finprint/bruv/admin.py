from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from global_finprint.bruv import models


admin.site.register(models.Bait)
admin.site.register(models.FrameType)
admin.site.register(models.Equipment)


class SetTagAdmin(MPTTModelAdmin):
    fields = ('parent', 'name', 'description', 'active')

admin.site.register(models.SetTag, SetTagAdmin)


class BenthicCategoryAdmin(MPTTModelAdmin):
    fields = ('parent', 'name', 'description', 'active')

admin.site.register(models.BenthicCategory, BenthicCategoryAdmin)

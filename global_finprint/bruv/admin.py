from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from global_finprint.bruv import models

admin.site.register(models.Bait)
admin.site.register(models.BaitContainer)
admin.site.register(models.FrameType)
admin.site.register(models.Equipment)


class SetTagAdmin(MPTTModelAdmin):
    fields = ('parent', 'name', 'description', 'active')

    def get_form(self, request, obj=None, **kwargs):
        form = super(SetTagAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['parent'].widget.can_add_related = False
        form.base_fields['parent'].widget.can_change_related = False
        return form


admin.site.register(models.SetTag, SetTagAdmin)


class BenthicCategoryAdmin(MPTTModelAdmin):
    fields = ('parent', 'name', 'description', 'active')

    def get_form(self, request, obj=None, **kwargs):
        form = super(BenthicCategoryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['parent'].widget.can_add_related = False
        form.base_fields['parent'].widget.can_change_related = False
        return form


admin.site.register(models.BenthicCategory, BenthicCategoryAdmin)

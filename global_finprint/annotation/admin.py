from django.contrib import admin
from django import forms
from mptt.admin import MPTTModelAdmin
from .models import animal, annotation, project, observation
from ..core.models import FinprintUser


class AnimalAdmin(admin.ModelAdmin):
    list_filter = ['family', 'genus']
    ordering = ['family', 'genus', 'species']
    search_fields = ['common_name', 'family', 'genus', 'species']

    def get_form(self, request, obj=None, **kwargs):
        form = super(AnimalAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['projects'].widget.can_add_related = False
        form.base_fields['projects'].widget.can_change_related = False
        return form

admin.site.register(animal.Animal, AnimalAdmin)
admin.site.register(animal.AnimalGroup)


class GlobalTagAdmin(MPTTModelAdmin):
    list_display = ('name', 'description')
    fields = ('parent', 'name', 'description')

admin.site.register(annotation.GlobalAttribute, GlobalTagAdmin)


class TagAdmin(MPTTModelAdmin):
    list_display = ('name', 'active', 'needs_review', 'not_selectable', 'lead_only', 'global_parent', 'project')
    fields = ('parent', 'name', 'description', 'global_parent', 'active', 'needs_review', 'not_selectable', 'lead_only', 'project')

    def get_form(self, request, obj=None, **kwargs):
        form = super(TagAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['parent'].widget.can_add_related = False
        form.base_fields['parent'].widget.can_change_related = False
        form.base_fields['global_parent'].widget.can_add_related = False
        form.base_fields['global_parent'].widget.can_change_related = False
        form.base_fields['project'].widget.can_add_related = False
        form.base_fields['project'].widget.can_change_related = False
        return form

admin.site.register(annotation.Attribute, TagAdmin)


class TagInline(admin.StackedInline):
    model = annotation.Attribute
    fields = ('parent', 'name', 'description', 'active', 'lead_only', 'project')

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(TagInline, self).get_formset(request, obj, **kwargs)
        formset.form.base_fields['parent'].widget.can_add_related = False
        formset.form.base_fields['parent'].widget.can_change_related = False
        return formset


class ProjectAdmin(admin.ModelAdmin):
    actions = None
    inlines = [TagInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].widget.can_add_related = False
        form.base_fields['user'].widget.can_change_related = False
        return form

    def has_delete_permission(self, request, obj=None):
        return (obj and obj.id != 1) or False

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = FinprintUser.get_lead_users()
        return super(ProjectAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(project.Project, ProjectAdmin)


class MeasurableAdminForm(forms.ModelForm):
    class Meta:
        model = observation.Measurable
        fields = ('name', 'description', 'active')
        widgets = {
            'name': forms.TextInput
        }


class MeasurableAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    form = MeasurableAdminForm

admin.site.register(observation.Measurable, MeasurableAdmin)


from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import animal, video, annotation, project


class AnimalAdmin(admin.ModelAdmin):
    list_filter = ['family', 'genus']
    ordering = ['family', 'genus', 'species']
    search_fields = ['common_name', 'family', 'genus', 'species']

admin.site.register(animal.Animal, AnimalAdmin)

admin.site.register(animal.AnimalGroup)
admin.site.register(video.AnnotationState)


class TagAdmin(MPTTModelAdmin):
    fields = ('parent', 'name', 'description', 'active', 'lead_only', 'project')

admin.site.register(annotation.Attribute, TagAdmin)


class TagInline(admin.StackedInline):
    model = annotation.Attribute
    fields = ('parent', 'name', 'description', 'active', 'lead_only', 'project')


class ProjectAdmin(admin.ModelAdmin):
    actions = None
    inlines = [TagInline]

    def has_delete_permission(self, request, obj=None):
        return (obj and obj.id != 1) or False

admin.site.register(project.Project, ProjectAdmin)

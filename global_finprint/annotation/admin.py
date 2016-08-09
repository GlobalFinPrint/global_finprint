from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import animal, video, annotation


class AnimalAdmin(admin.ModelAdmin):
    list_filter = ['family', 'genus']
    ordering = ['family', 'genus', 'species']
    search_fields = ['common_name', 'family', 'genus', 'species']

admin.site.register(animal.Animal, AnimalAdmin)

admin.site.register(animal.AnimalGroup)
admin.site.register(video.AnnotationState)
admin.site.register(annotation.Attribute, MPTTModelAdmin)

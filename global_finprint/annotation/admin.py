from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import animal, video, annotation


admin.site.register(animal.AnimalGroup)
admin.site.register(animal.Animal)
admin.site.register(video.AnnotationState)
admin.site.register(annotation.Attribute, MPTTModelAdmin)

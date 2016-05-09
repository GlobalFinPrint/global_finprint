from django.contrib import admin

from global_finprint.annotation.models import animal, video


admin.site.register(animal.AnimalGroup)
admin.site.register(animal.Animal)
admin.site.register(video.AnnotationState)

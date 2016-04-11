from django.contrib import admin

from global_finprint.annotation import models


admin.site.register(models.AnimalBehavior)
admin.site.register(models.AnimalGroup)
admin.site.register(models.Animal)
admin.site.register(models.AnnotationState)

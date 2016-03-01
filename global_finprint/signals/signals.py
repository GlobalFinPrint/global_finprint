from django.db.models.signals import post_save
from django.contrib.auth.models import User
from global_finprint.annotation.models import Annotator
from global_finprint.core.models import Affiliation
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_annotator(**kwargs):
    new_annotator = Annotator(user=kwargs['instance'], affiliation=Affiliation.objects.get(pk=0))
    new_annotator.save()

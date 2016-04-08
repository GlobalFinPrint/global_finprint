from django.db.models.signals import post_save
from django.contrib.auth.models import User
from global_finprint.core.models import Affiliation, FinprintUser
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_annotator(**kwargs):
    if kwargs.get('created', True) and not kwargs.get('raw', False):
        new_annotator = FinprintUser(user=kwargs['instance'], affiliation=Affiliation.objects.get(pk=0))
        new_annotator.save()

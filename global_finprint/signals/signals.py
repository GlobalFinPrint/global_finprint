from django.db.models.signals import post_save
from django.contrib.auth.models import User
from global_finprint.core.models import FinprintUser
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_annotator(**kwargs):
    if kwargs.get('created', True) and not kwargs.get('raw', False):
        new_user = kwargs['instance']
        new_user.groups = [1, 2] if new_user.is_superuser else [1]
        new_user.save()
        new_annotator = FinprintUser(user=new_user, affiliation_id=0)
        new_annotator.save()

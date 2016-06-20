from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from .models import FinprintUser


class FinprintAuth(ModelBackend):
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            FinprintUser.objects.get(user=user)
            return user
        except (User.DoesNotExist, FinprintUser.DoesNotExist):
            return None

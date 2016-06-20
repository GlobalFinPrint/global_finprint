from django.contrib.auth.mixins import UserPassesTestMixin
from ..core.models import FinprintUser


class UserAllowedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.user_allowed(self.request.user)

    @staticmethod
    def user_allowed(user):
        try:
            FinprintUser.objects.get(user_id=user.id)
            return user.is_authenticated() and (user.is_superuser or user.groups.filter(id=1).exists())
        except FinprintUser.DoesNotExist:
            return False

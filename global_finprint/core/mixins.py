from django.contrib.auth.mixins import UserPassesTestMixin
from ..core.models import FinprintUser


class UserAllowedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.user_allowed(self.request.user)

    @staticmethod
    def user_allowed(user):
        return user.is_authenticated() and (user.is_superuser or FinprintUser.objects.filter(user=user).exists())

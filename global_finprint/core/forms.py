from django.contrib.auth.forms import AuthenticationForm
from django.forms import ValidationError
from .models import FinprintUser


class FinprintAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        try:
            FinprintUser.objects.get(user=user)
            return super(FinprintAuthenticationForm, self).confirm_login_allowed(user)
        except FinprintUser.DoesNotExist:
            raise ValidationError('Missing user profile. Please contact administrator.',
                                  code='missing_finprintuser')

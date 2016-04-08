from django.forms import ChoiceField, RadioSelect
from django.contrib.admin import site
from django.contrib.auth import admin, forms, models
from .models import Affiliation


class UserCreationForm(forms.UserCreationForm):
    role = ChoiceField(
        choices=[('superuser', 'Superuser'), ('lead', 'Lead'), ('annotator', 'Annotator')],
        widget=RadioSelect()
    )

    class Meta:
        model = models.User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field in ['first_name', 'last_name', 'email', 'role']:
            self.fields[field].required = True
        self.fields['role'].initial = 'annotator'

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=True)
        role = self.cleaned_data.get('role')
        user.groups = [2] if role == 'annotator' else [1, 2]
        if role == 'superuser':
            user.is_superuser = True
            user.is_staff = True
        user.save()
        return user


class UserAdmin(admin.UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'role'),
        }),
    )
    add_form = UserCreationForm


site.unregister(models.User)
site.register(models.User, UserAdmin)
site.register(Affiliation)

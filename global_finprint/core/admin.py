from django.contrib.admin import site
from django.contrib.auth import admin, forms, models
from .models import Affiliation


class UserCreationForm(forms.UserCreationForm):
    class Meta:
        model = models.User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['first_name', 'last_name', 'email']:
            self.fields[field].required = True


class UserAdmin(admin.UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email'),
        }),
    )
    add_form = UserCreationForm


site.unregister(models.User)
site.register(models.User, UserAdmin)
site.register(Affiliation)

from django.forms import ChoiceField, ModelChoiceField, RadioSelect
from django.contrib.admin import site, ModelAdmin, StackedInline
from django.contrib.auth import admin, forms, models
from .models import Affiliation, FinprintUser, Team


class UserCreationForm(forms.UserCreationForm):
    affiliation = ModelChoiceField(
        queryset=Affiliation.objects.all(),
        empty_label=None
    )
    role = ChoiceField(
        choices=[('superuser', 'Superuser'), ('lead', 'Lead'), ('annotator', 'Annotator')],
        widget=RadioSelect()
    )

    class Meta:
        model = models.User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field in ['first_name', 'last_name', 'email', 'affiliation', 'role']:
            self.fields[field].required = True
        self.fields['role'].initial = 'annotator'
        self.fields['affiliation'].initial = 0

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=True)
        role = self.cleaned_data.get('role')
        user.groups = [2] if role == 'annotator' else [1, 2]
        if role == 'superuser':
            user.is_superuser = True
            user.is_staff = True
        user.save()
        FinprintUser(
            user=user,
            affiliation=self.cleaned_data.get('affiliation')
        ).save()
        return user


class FinprintUserInline(StackedInline):
    actions = None
    model = FinprintUser
    fields = ('affiliation',)


class UserAdmin(admin.UserAdmin):
    actions = None
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'groups')
        }),
    )
    inlines = (FinprintUserInline,)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'affiliation', 'role'),
        }),
    )
    add_form = UserCreationForm

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide FinprintUserInline in the add view
            if isinstance(inline, FinprintUserInline) and obj is None:
                continue
            yield inline.get_formset(request, obj), inline

    # disable the delete button and remove delete from actions
    def has_delete_permission(self, request, obj=None):
        return False


class FinprintUserAdmin(ModelAdmin):
    actions = None
    fields = ('user', 'affiliation')
    ordering = ['affiliation__name', 'user__last_name', 'user__first_name']


site.unregister(models.User)
site.register(models.User, UserAdmin)
site.register(Affiliation)
site.register(Team)
site.register(FinprintUser, FinprintUserAdmin)

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

    # disable the delete button and remove delete from actions
    def has_delete_permission(self, request, obj=None):
        return False


class UserAdmin(admin.UserAdmin):
    actions = None
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'is_active', 'groups', 'password')
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
    list_display = ('username', 'last_name', 'first_name', 'email', 'is_active')
    list_filter = ['finprintuser__affiliation', 'groups', 'is_active', 'is_superuser']
    search_fields = ['last_name', 'first_name', 'username', 'email', 'finprintuser__affiliation__name']

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide FinprintUserInline in the add view
            if isinstance(inline, FinprintUserInline) and obj is None:
                continue
            yield inline.get_formset(request, obj), inline

    # disable the delete button and remove delete from actions
    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # if user is being set to "inactive", remove any assignments that are not complete
        if 'is_active' in form.changed_data and not obj.is_active:

            for assignment in obj.finprintuser.assignment_set.all():
                assignment.remove(unfinished_only=True)
        obj.save()


class FinprintUserAdmin(ModelAdmin):
    actions = None
    fields = ('user', 'affiliation')
    ordering = ['affiliation__name', 'user__last_name', 'user__first_name']
    list_filter = ['affiliation__name']
    search_fields = ['affiliation__name', 'user__last_name', 'user__first_name']

    # disable the delete button and remove delete from actions
    def has_delete_permission(self, request, obj=None):
        return False


site.unregister(models.User)
site.register(models.User, UserAdmin)
site.register(Affiliation)
site.register(Team)
site.register(FinprintUser, FinprintUserAdmin)

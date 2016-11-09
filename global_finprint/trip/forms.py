from django import forms
from django.db.models import Count
from django.db.models.functions import Lower
from crispy_forms.helper import FormHelper
import crispy_forms.layout as cfl
import crispy_forms.bootstrap as cfb
from bootstrap3_datetime.widgets import DateTimePicker
from ..habitat.models import Location, Region, Reef
from .models import Trip
from ..core.models import Team


datepicker_opts = {"format": "MMMM DD YYYY", "showClear": True, "extraFormats": ["D/M/Y"]}


class TripForm(forms.ModelForm):
    start_date = forms.DateField(
        input_formats=['%B %d %Y'],
        widget=DateTimePicker(options=datepicker_opts)
    )
    end_date = forms.DateField(
        input_formats=['%B %d %Y'],
        widget=DateTimePicker(options=datepicker_opts)
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.annotate(Count('site__reef')).filter(site__reef__count__gt=0).all()
    )

    class Meta:
        model = Trip
        fields = ['source', 'team', 'location', 'start_date', 'end_date', 'boat', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline trip form-group-sm'
        self.helper.form_method = "post"
        help_text = '<small class="help-block">*Required Field &nbsp;&nbsp;&nbsp; **Note: If code is left blank, ' \
                    'it will be automatically generated.</small>'
        self.helper.layout = cfl.Layout(
            cfl.Fieldset(
                *([None] + self.Meta.fields)
            ),
            cfl.Div(
                cfl.Div(
                    cfl.HTML(help_text),
                    css_class='pull-left'),
                cfl.Div(
                    cfb.FormActions(
                        cfl.HTML("""<a role="button" class="btn btn-default btn-fp cancel-button"
                        href="{% url "trip_list" %}">Cancel</a>"""),
                        cfl.Submit('save', 'Save trip', css_class='btn-fp')),
                    css_class='pull-right')))
        self.fields['code'].label += '**'


class TripSearchForm(forms.Form):
    search_start_date = forms.DateField(required=False,
                                        input_formats=['%B %d %Y'],
                                        widget=DateTimePicker(options=datepicker_opts))
    search_end_date = forms.DateField(required=False,
                                      input_formats=['%B %d %Y'],
                                      widget=DateTimePicker(options=datepicker_opts))
    region = forms.ModelChoiceField(required=False,
                                    queryset=Region.objects.all().order_by(Lower('name')))
    location = forms.ModelChoiceField(required=False,
                                      queryset=Location.objects.filter(trip__in=Trip.objects.all())
                                      .distinct().order_by(Lower('name'), Lower('code')))
    team = forms.ModelChoiceField(required=False,
                                  queryset=Team.objects.filter(trip__in=Trip.objects.all())
                                  .distinct().order_by(Lower('lead__user__username'), Lower('sampler_collaborator')))
    reef = forms.ModelChoiceField(required=False,
                                  queryset=Reef.old_manager.order_by(Lower('site__name'), Lower('name'))
                                  .select_related('site'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline trip-search form-group-sm'
        self.helper.form_method = "get"
        self.helper.layout = cfl.Layout(
            cfl.Div(
                'search_start_date',
                'search_end_date',
                'region',
                'location',
                'team',
                'reef'),
            cfl.Div(
                cfb.FormActions(
                    cfl.HTML("""<a role="button" class="btn btn-default cancel-button btn-fp"
                    href="{% url "trip_list" %}">Reset</a>"""),
                    cfl.Submit('', 'Search', css_class='btn-fp')),
                css_class='row pull-right'))

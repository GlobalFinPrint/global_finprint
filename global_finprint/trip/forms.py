from django import forms
from django.db.models import Count
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
import crispy_forms.layout as cfl
import crispy_forms.bootstrap as cfb
from bootstrap3_datetime.widgets import DateTimePicker
from ..habitat.models import Location, Region, Reef, ReefHabitat
from .models import Trip
from ..core.models import Team


datepicker_opts = {"format": "MMMM DD YYYY"}


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
        #if 'instance' in kwargs and kwargs['instance']:
        #    self.helper.form_action = reverse('trip_update', args=[kwargs['instance'].pk])
        #else:
        #    self.helper.form_action = reverse('trip_list')
        self.helper.form_method = "post"
        help_text = '<small class="help-block">**Note: If code is left blank, ' \
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
                        cfl.HTML("""<a role="button" class="btn btn-default cancel-button"
                        href="{% url "trip_list" %}">Cancel</a>"""),
                        cfl.Submit('save', 'Save trip')),
                    css_class='pull-right'),
                css_class='row'))
        self.fields['code'].label += '**'


class TripSearchForm(forms.Form):
    search_start_date = forms.DateField(required=False,
                                        input_formats=['%B %d %Y'],
                                        widget=DateTimePicker(options=datepicker_opts))
    search_end_date = forms.DateField(required=False,
                                      input_formats=['%B %d %Y'],
                                      widget=DateTimePicker(options=datepicker_opts))
    region = forms.ModelChoiceField(required=False,
                                    queryset=Region.objects.all())
    location = forms.ModelChoiceField(required=False,
                                      queryset=Location.objects.filter(trip__in=Trip.objects.all()).distinct())
    team = forms.ModelChoiceField(required=False,
                                  queryset=Team.objects.filter(trip__in=Trip.objects.all()).distinct())
    reef = forms.ModelChoiceField(required=False,
                                  queryset=Reef.objects.order_by('site__name', 'name'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline trip-search form-group-sm'
        self.helper.form_method = "get"
        self.helper.layout = cfl.Layout(
            cfl.Fieldset(
                'Filter by:',
                'search_start_date',
                'search_end_date',
                'region',
                'location',
                'team',
                'reef'),
            cfl.Div(
                cfb.FormActions(
                    cfl.HTML("""<a role="button" class="btn btn-default cancel-button"
                    href="{% url "trip_list" %}">Reset search</a>"""),
                    cfl.Submit('', 'Search trips')),
                css_class='row pull-right'))

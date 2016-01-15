from django import forms
from django.db.models import Count
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions
from bootstrap3_datetime.widgets import DateTimePicker
from ..habitat.models import Location, Region
from .models import Team, Trip


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
        fields = ['code', 'team', 'start_date', 'end_date', 'location', 'boat']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline trip'
        if 'instance' in kwargs and kwargs['instance']:
            self.helper.form_action = reverse('trip_update', args=[kwargs['instance'].pk])
        else:
            self.helper.form_action = reverse('trip_list')
        self.helper.form_method = "post"
        self.helper.layout.append(
            FormActions(HTML("""<a role="button" class="btn btn-default cancel-button"
            href="{% url "trip_list" %}">Cancel</a>"""),
                        Submit('save', 'Save trip')))


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline trip-search'
        self.helper.form_action = reverse('trip_list')
        self.helper.form_method = "get"
        self.helper.layout.append(
            FormActions(HTML("""<a role="button" class="btn btn-default cancel-button"
                href="{% url "trip_list" %}">Reset search</a>"""),
                        Submit('', 'Search trips')))

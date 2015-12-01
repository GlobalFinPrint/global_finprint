from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions
from bootstrap3_datetime.widgets import DateTimePicker
from global_finprint.habitat.models import Location
from .models import Team, Trip
from global_finprint.trip import models
from django.core.urlresolvers import reverse


class TripForm(forms.ModelForm):
    class Meta:
        model = models.Trip
        fields = ['team', 'start_date', 'end_date', 'location', 'boat',]
        widgets = {
            'start_date': DateTimePicker(options={
                "format": "YYYY-MM-DD",
                "pickTime": False}),
            'end_date': DateTimePicker(options={
                "format": "YYYY-MM-DD",
                "pickTime": False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline trip'
        self.helper.form_action = reverse('trip_create')
        self.helper.form_method = "post"
        self.helper.layout.append(FormActions(Submit('save', 'Add trip')))


class TripSearchForm(forms.Form):
    start_date = forms.DateField(required=False, widget=DateTimePicker(options={
        "format": "YYYY-MM-DD",
        "pickTime": False}))
    end_date = forms.DateField(required=False, widget=DateTimePicker(options={
        "format": "YYYY-MM-DD",
        "pickTime": False}))
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

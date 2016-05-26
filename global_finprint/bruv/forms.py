from django import forms
from crispy_forms.helper import FormHelper
from bootstrap3_datetime.widgets import DateTimePicker
from .models import Set, EnvironmentMeasure, Bait
from ..trip.models import Trip
from ..habitat.models import Reef, ReefType


timepicker_opts = {"format": "HH:mm", "showClear": True}
datepicker_opts = {"format": "MMMM DD YYYY", "showClear": True}


class SetForm(forms.ModelForm):
    set_date = forms.DateField(
        input_formats=['%B %d %Y'],
        widget=DateTimePicker(options=datepicker_opts)
    )
    drop_time = forms.TimeField(
        input_formats=['%H:%M'],
        widget=DateTimePicker(options=timepicker_opts, icon_attrs={'class': 'glyphicon glyphicon-time'})
    )
    haul_time = forms.TimeField(
        input_formats=['%H:%M'],
        widget=DateTimePicker(options=timepicker_opts, icon_attrs={'class': 'glyphicon glyphicon-time'})
    )
    reef = forms.ModelChoiceField(
        queryset=Reef.objects.all()
    )
    habitat = forms.ModelChoiceField(
        queryset=ReefType.objects.all()
    )

    class Meta:
        model = Set
        fields = ['trip', 'code', 'set_date', 'latitude', 'longitude', 'depth',
                  'drop_time', 'haul_time', 'reef', 'habitat', 'equipment', 'bait', 'visibility',
                  'reef_habitat',]
        exclude = ('reef_habitat',)
        widgets = {
            'trip': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        try:
            trip_pk = kwargs.pop('trip_pk')
        except KeyError:
            trip_pk = False

        super().__init__(*args, **kwargs)

        if trip_pk:
            self.fields['reef'].queryset = Trip.objects.get(pk=trip_pk).location.reef_set

        self.fields['visibility'].choices = \
            sorted(self.fields['visibility'].choices,
                   key=lambda _: _[0].isdigit() and int(_[0]) or _[0] == '' and -1 or 100)
        self.fields['visibility'].choices[0] = (None, '---')

        self.helper = FormHelper(self)
        self.helper.form_tag = False


class EnvironmentMeasureForm(forms.ModelForm):
    class Meta:
        model = EnvironmentMeasure
        fields = ['water_temperature', 'salinity',
                  'conductivity', 'dissolved_oxygen', 'current_flow',
                  'current_direction', 'tide_state', 'estimated_wind_speed',
                  'wind_direction', 'cloud_cover', 'surface_chop']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

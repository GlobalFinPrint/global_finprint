from django import forms
from global_finprint.bruv.models import Set, Observation, EnvironmentMeasure
from global_finprint.trip.models import Trip
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions
from bootstrap3_datetime.widgets import DateTimePicker


datepicker_opts = {"format": "MMMM DD YYYY HH:mm", "pickSeconds": False}


class SetForm(forms.ModelForm):
    drop_time = forms.DateTimeField(
        input_formats=['%B %d %Y %H:%M'],
        widget=DateTimePicker(options=datepicker_opts)
    )
    collection_time = forms.DateTimeField(
        required=False,
        input_formats=['%B %d %Y %H:%M'],
        widget=DateTimePicker(options=datepicker_opts)
    )

    class Meta:
        model = Set
        fields = ['trip', 'latitude', 'longitude', 'depth',
                  'drop_time', 'collection_time', 'reef',
                  'equipment', 'visibility', 'bait', 'bait_oiled']
        widgets = {
            'trip': forms.HiddenInput()
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
        self.helper.form_class = 'form-inline set'
        self.helper.form_action = "{{ action }}"
        self.helper.form_method = "post"
        self.helper.form_tag = False


class ObservationForm(forms.ModelForm):
    initial_observation_time = forms.DateTimeField(
        input_formats=['%B %d %Y %H:%M'],
        widget=DateTimePicker(options=datepicker_opts)
    )

    class Meta:
        model = Observation
        fields = ['initial_observation_time',
                  'animal', 'sex', 'stage', 'length', 'behavior',
                  'set', 'video_annotator']
        widgets = {
            'set': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline obs'
        self.helper.form_action = "{{ action }}"
        self.helper.form_method = "post"
        self.helper.layout.append(
            FormActions(HTML("""<a role="button" class="btn btn-default cancel-button"
            href="{% url "trip_set_list" trip_pk %}">Cancel</a>"""),
                        Submit('save', 'Save Observation')))


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
        self.helper.form_class = 'form-inline env'
        self.helper.form_action = "{{ action }}"
        self.helper.form_method = "post"
        self.helper.form_tag = False

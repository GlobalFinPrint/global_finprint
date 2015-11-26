from django.forms import ModelForm, HiddenInput
from global_finprint.bruv.models import Set, Observation, EnvironmentMeasure
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions
from bootstrap3_datetime.widgets import DateTimePicker


class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = ['trip', 'latitude', 'longitude', 'depth',
                  'drop_time', 'collection_time', 'tide_state',
                  'reef', 'equipment', 'visibility',
                  'bait', 'bait_oiled']
        widgets = {
                    'trip': HiddenInput(),
                    'drop_time': DateTimePicker(options={
                        "format": "YYYY-MM-DD HH:mm",
                        "pickSeconds": False}),
                    'collection_time': DateTimePicker(options={
                        "format": "YYYY-MM-DD HH:mm",
                        "pickSeconds": False}),
                }

    def __init__(self, *args, **kwargs):
        try:
            nocancel = kwargs.pop('nocancel')
        except KeyError:
            nocancel = False
        super().__init__(*args, **kwargs)
        self.fields['visibility'].choices = \
            sorted(self.fields['visibility'].choices, key=lambda _: _[0].isdigit() and int(_[0])
                                                                    or _[0] == '' and -1 or 100)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline set'
        self.helper.form_action = "{{ action }}"
        self.helper.form_method = "post"
        self.helper.layout.append(FormActions(Submit('save', 'Save Set')))
        if not nocancel:
            self.helper.layout.append(
                FormActions(
                    HTML("""<a role="button" class="btn btn-default cancel-button"
                        href="{% url "trip_set_list" trip_pk %}">Cancel</a>"""),
                )
            )
            self.helper.form_class += ' with-cancel'


class ObservationForm(ModelForm):
    class Meta:
        model = Observation
        fields = ['initial_observation_time',
                  'animal', 'sex', 'stage', 'length', 'behavior',
                  'set', 'video_annotator']
        widgets = {
            'set': HiddenInput(),
            'initial_observation_time': DateTimePicker(options={
                "format": "YYYY-MM-DD HH:mm",
                "pickSeconds": False}),
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


class EnvironmentMeasureForm(ModelForm):
    class Meta:
        model = EnvironmentMeasure
        fields = ['set', 'measurement_time', 'water_temperature', 'salinity',
                  'conductivity', 'dissolved_oxygen', 'current_flow',
                  'current_direction']
        widgets = {
            'set': HiddenInput(),
            'measurement_time': DateTimePicker(options={
                "format": "YYYY-MM-DD HH:mm",
                "pickSeconds": False})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline env'
        self.helper.form_action = "{{ action }}"
        self.helper.form_method = "post"
        self.helper.layout.append(
            FormActions(HTML("""<a role="button" class="btn btn-default cancel-button"
            href="{% url "trip_set_list" trip_pk %}">Cancel</a>"""),
                        Submit('save', 'Save Environment Measure')))

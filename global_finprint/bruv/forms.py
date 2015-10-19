from django.forms import ModelForm
from global_finprint.bruv.models import Set, Observation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions
from bootstrap3_datetime.widgets import DateTimePicker


class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = ['drop_time', 'collection_time', 'time_bait_gone', 'equipment', 'depth', 'reef', 'trip']
        widgets = {
                    'drop_time': DateTimePicker(options={
                        "format": "YYYY-MM-DD HH:mm",
                        "pickSeconds": False}),
                    'collection_time': DateTimePicker(options={
                        "format": "YYYY-MM-DD HH:mm",
                        "pickSeconds": False}),
                    'time_bait_gone': DateTimePicker(options={
                        "format": "YYYY-MM-DD HH:mm",
                        "pickSeconds": False}),
                }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = "{{ action }}"
        self.helper.form_method = "post"
        self.helper.layout.append(
            FormActions(HTML("""<a role="button" class="btn btn-default" href="{% url "trip_list" %}">Cancel</a>"""),
                        Submit('save', 'Save')))

#
# class ObservedAnimalForm(ModelForm):
#     class Meta:
#         model = ObservedAnimal
#         fields = ['animal', 'sex', 'stage', 'length', 'activity', 'behavior']


class ObservationForm(ModelForm):
    class Meta:
        model = Observation
        fields = ['initial_observation_time',
                  'animal', 'sex', 'stage', 'length', 'activity', 'behavior',
                  'maximum_number_observed', 'maximum_number_observed_time',
                  'set', 'observer',
                  ]
        widgets = {
            'initial_observation_time': DateTimePicker(options={
                "format": "YYYY-MM-DD HH:mm",
                "pickSeconds": False}),
            'maximum_number_observed_time': DateTimePicker(options={
                "format": "YYYY-MM-DD HH:mm",
                "pickSeconds": False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = "{{ action }}"
        self.helper.form_method = "post"
        self.helper.layout.append(
            FormActions(HTML("""<a role="button" class="btn btn-default" href="{% url "trip_list" %}">Cancel</a>"""),
                        Submit('save', 'Save')))
#
#
# ObservationFormSet = inlineformset_factory(
#     ObservedAnimal,
#     Observation,
#     fields=(
#         # 'animal', 'sex', 'stage', 'length', 'activity', 'behavior',
#         'initial_observation_time', 'maximum_number_observed',
#         'maximum_number_observed_time', 'set', 'observer'
#     )
# )

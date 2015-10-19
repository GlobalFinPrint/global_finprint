from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions
from bootstrap3_datetime.widgets import DateTimePicker

from global_finprint.trip import models


class TripForm(ModelForm):
    class Meta:
        model = models.Trip
        fields = ['team', 'start_date', 'end_date', 'location', 'boat', 'type']
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
        self.helper.form_action = "{{ action }}"
        self.helper.form_method = "post"
        self.helper.layout.append(
            FormActions(HTML("""<a role="button" class="btn btn-default" href="{% url "trip_list" %}">Cancel</a>"""),
                        Submit('save', 'Save')))


from django.forms import ModelForm
from django.forms.formsets import formset_factory
from global_finprint.trip import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Layout, Fieldset
from crispy_forms.bootstrap import FormActions


class TripForm(ModelForm):
    class Meta:
        model = models.Trip
        fields = ['team', 'start_date', 'end_date', 'location', 'boat', 'type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = "{{ action }}"
        self.helper.form_method = "post"
        self.helper.layout.append(
            FormActions(HTML("""<a role="button" class="btn btn-default" href="{% url "trip_list" %}">Cancel</a>"""),
                        Submit('save', 'Save')))


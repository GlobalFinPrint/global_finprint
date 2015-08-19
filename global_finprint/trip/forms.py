from django.forms import ModelForm
from global_finprint.trip import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions

class TripForm(ModelForm):

    class Meta:
        model = models.Trip
        fields = ['name', 'location', 'start_datetime', 'end_datetime', 'team', 'boat', 'type']

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(FormActions(
                    HTML("""<a role="button" class="btn btn-default"
                         href="{% url "trip_list" %}">Cancel</a>"""),
                    Submit('save', 'Submit'),))
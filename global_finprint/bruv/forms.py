from django.forms import ModelForm
from global_finprint.bruv.models import Set
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML
from crispy_forms.bootstrap import FormActions


class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = ['drop_time', 'collection_time', 'time_bait_gone', 'equipment', 'depth', 'reef', 'trip']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = "{{ action }}"
        self.helper.form_method = "post"
        self.helper.layout.append(
            FormActions(HTML("""<a role="button" class="btn btn-default" href="{% url "trip_list" %}">Cancel</a>"""),
                        Submit('save', 'Save')))



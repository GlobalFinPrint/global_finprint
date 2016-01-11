from django import forms
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, HTML
from .models import Video, VideoAnnotator, Annotator
from ..trip.models import Trip, Team
from ..habitat.models import Location, Region


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False


class VideoAnnotatorSearchForm(forms.Form):
    trip = forms.ModelChoiceField(required=False,
                                  queryset=Trip.objects.all())
    team = forms.ModelChoiceField(required=False,
                                  queryset=Team.objects.all())
    location = forms.ModelChoiceField(required=False,
                                      queryset=Location.objects.all())
    region = forms.ModelChoiceField(required=False,
                                    queryset=Region.objects.all())
    annotator = forms.ModelChoiceField(required=False,
                                       queryset=Annotator.objects.all(),
                                       label='Assigned annotator')
    number_assigned = forms.ChoiceField(required=False,
                                        choices=[(None, '----'), (0, 0), (1, 1), (2, 2), ('3+', '3+')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline video-annotator-search'
        self.helper.form_action = reverse('video_annotator_list')
        self.helper.form_method = "get"
        self.helper.layout.append(
                FormActions(HTML("""<a role="button" class="btn btn-default cancel-button"
                href="{% url "video_annotator_list" %}">Reset search</a>"""),
                            Submit('', 'Search videos')))


class VideoAnnotatorForm(forms.ModelForm):
    class Meta:
        model = VideoAnnotator
        fields = ['video', 'annotator', 'assigned_by']
        widgets = {'assigned_by': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline video-annotator'
        self.helper.form_action = reverse('video_annotator_list')
        self.helper.layout.append(
                FormActions(HTML("""<a role="button" class="btn btn-default cancel-button"
            href="{% url "video_annotator_list" %}">Cancel</a>"""),
                            Submit('save', 'Assign video')))

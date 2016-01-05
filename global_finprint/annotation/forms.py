from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, HTML
from .models import Video, VideoAnnotator


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False


class VideoAnnotatorForm(forms.ModelForm):
    class Meta:
        model = VideoAnnotator
        fields = ['annotator', 'video']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline video-annotator'
        self.helper.layout.append(
                FormActions(HTML("""<a role="button" class="btn btn-default cancel-button"
            href="{% url "video_annotator_list" %}">Cancel</a>"""),
                            Submit('save', 'Assign video')))

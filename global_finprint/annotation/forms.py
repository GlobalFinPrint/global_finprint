from django import forms
from crispy_forms.helper import FormHelper
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

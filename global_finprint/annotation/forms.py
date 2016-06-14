from django import forms
from crispy_forms.helper import FormHelper
from .models.video import Video
from boto import exception as BotoException
from boto.s3.connection import S3Connection
from django.conf import settings
import re


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.fields['file'] = forms.ChoiceField(choices=self.get_filenames())

    def get_filenames(self):
        pattern = re.compile('\.\w+$')
        file_names = [('', '---')]
        try:
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            files = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME).list()
            file_names += [(f.name, f.name) for f in files if pattern.search(f.name)]
        except BotoException.S3ResponseError:
            pass
        return file_names

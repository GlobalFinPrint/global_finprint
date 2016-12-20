from django import forms
from crispy_forms.helper import FormHelper
from .models.video import Video
from boto import exception as BotoException
from boto.s3.connection import S3Connection
from django.conf import settings
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import re


class FlexibleChoiceField(forms.ChoiceField):
    def validate(self, value):
        forms.Field.validate(self, value)


class SingleSelectizeWidget(forms.Select):
    template = '<select class="selectize form-control"{}>'

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        if (value, value) not in self.choices:
            self.choices += [(value, value)]
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html(self.template, flatatt(final_attrs))]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output))


class RemoveWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        html = '<a href="#" class="remove">Remove</a>'
        return mark_safe(html)


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['file', 'source', 'path', 'primary', 'remove_row']

    source = forms.CharField(required=False, label='File system/source')
    path = forms.CharField(required=False, label='Path')
    primary = forms.ChoiceField(required=False, choices=[0], label='Annotation video', widget=forms.RadioSelect)
    remove_row = forms.Field(required=False, label='', widget=RemoveWidget)

    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.fields['file'] = FlexibleChoiceField(choices=self.get_filenames(),
                                                  required=False,
                                                  label='File name',
                                                  widget=SingleSelectizeWidget)

    def get_filenames(self):
        pattern = re.compile('\.\w+$')
        file_names = [('', '(None)')]
        try:
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            files = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME).list()
            file_names += [(f.name, f.name) for f in files if pattern.search(f.name)]
        except BotoException.S3ResponseError:
            pass
        return file_names

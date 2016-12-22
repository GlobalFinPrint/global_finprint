from django import forms
from crispy_forms.helper import FormHelper
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
    template = '<div class="sub-control"><select class="selectize form-control" name="{}" {}>'

    def render(self, name, values, attrs=None, choices=()):
        output = []
        for value in values:
            if value is None:
                value = ''
            if (value, value) not in self.choices:
                self.choices += [(value, value)]
            final_attrs = self.build_attrs(attrs, name=name)
            output.append(format_html(self.template, name, flatatt(final_attrs)))
            options = self.render_options(choices, [value])
            if options:
                output.append(options)
            output.append('</select></div>')
        return mark_safe('\n'.join(output))


class MultiRowTextInput(forms.Widget):
    template = '<div class="sub-control"><input class="form-control textInput" {} type="text" value="{}" {} /></div>'

    def render(self, name, value, attrs=None):
        html = ''
        for val in value:
            html += self.template.format(name, '' if val is None else val, flatatt(attrs))
        return mark_safe(html)


class MultiRowRadioSelect(forms.Widget):
    template = '<div class="sub-control"><input class="radio" {} type="radio" {} {}/></div>'

    def render(self, name, value, attrs=None):
        html = ''
        for val in value:
            html += self.template.format(name, 'checked ' if val else '', flatatt(attrs))
        return mark_safe(html)


class RemoveWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        html = ''
        for _ in value:
            html += '<div class="sub-control"><a href="#" class="remove">Remove</a></div>'
        return mark_safe(html)


class MultiCharField(forms.CharField):
    def to_python(self, value):
        return list(super(MultiCharField, self).to_python(value))


class VideoForm(forms.Form):
    file = FlexibleChoiceField(required=False, label='File name', widget=SingleSelectizeWidget)
    source = MultiCharField(required=False, label='File system/source', max_length=100, widget=MultiRowTextInput)
    path = MultiCharField(required=False, label='Path', max_length=100, widget=MultiRowTextInput)
    primary = forms.ChoiceField(required=False, label='Annotation video', widget=MultiRowRadioSelect)
    remove_row = forms.Field(required=False, label='', widget=RemoveWidget)

    field_order = ['file', 'source', 'path', 'primary', 'remove_row']

    def __init__(self, *args, **kwargs):
        video = kwargs.pop('instance', None)
        super(VideoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.fields['file'].choices = self.get_filenames()
        self.fields['file'].initial = [None]
        self.fields['source'].initial = [None]
        self.fields['path'].initial = [None]
        self.fields['primary'].initial = [True]
        self.fields['remove_row'].initial = [0]

        if video is not None:
            video_files = video.files.order_by('rank')
            self.fields['file'].initial = list(f.file for f in video_files)
            self.fields['source'].initial = list(f.source_folder for f in video_files)
            self.fields['path'].initial = list(f.path for f in video_files)
            self.fields['primary'].initial = list(f.primary for f in video_files)
            self.fields['remove_row'].initial = list(range(max(video_files.count(), 1)))

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

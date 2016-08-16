from django import forms
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.templatetags.staticfiles import static
from crispy_forms.helper import FormHelper
import crispy_forms.layout as cfl
import crispy_forms.bootstrap as cfb
from bootstrap3_datetime.widgets import DateTimePicker
from .models import Set, EnvironmentMeasure, Bait, Equipment, SetTag
from ..trip.models import Trip
from ..habitat.models import Reef, ReefType


timepicker_opts = {"format": "HH:mm", "showClear": True}
datepicker_opts = {"format": "MMMM DD YYYY", "showClear": True}


class SetForm(forms.ModelForm):
    set_date = forms.DateField(
        input_formats=['%B %d %Y'],
        widget=DateTimePicker(options=datepicker_opts)
    )
    drop_time = forms.TimeField(
        input_formats=['%H:%M'],
        widget=DateTimePicker(options=timepicker_opts, icon_attrs={'class': 'glyphicon glyphicon-time'})
    )
    haul_time = forms.TimeField(
        input_formats=['%H:%M'],
        widget=DateTimePicker(options=timepicker_opts, icon_attrs={'class': 'glyphicon glyphicon-time'})
    )
    reef = forms.ModelChoiceField(
        queryset=Reef.objects.all()
    )
    habitat = forms.ModelChoiceField(
        queryset=ReefType.objects.all()
    )

    class Meta:
        model = Set
        fields = ['trip', 'set_date', 'latitude', 'longitude', 'depth',
                  'drop_time', 'haul_time', 'reef', 'habitat', 'equipment', 'bait',
                  'reef_habitat', 'code']
        exclude = ('reef_habitat',)
        widgets = {
            'trip': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        try:
            trip_pk = kwargs.pop('trip_pk')
        except KeyError:
            trip_pk = False

        super().__init__(*args, **kwargs)

        if trip_pk:
            self.fields['reef'].queryset = Trip.objects.get(pk=trip_pk).location.reef_set

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.fields['code'].label += '**'
        help_text = '<small class="help-block">**Note: If code is left blank, ' \
                    'it will be automatically generated.</small>'
        self.helper.layout.append(cfl.Div(cfl.HTML(help_text)))


class SetSearchForm(forms.Form):
    set_date = forms.DateField(required=False,
                               input_formats=['%B %d %Y'],
                               widget=DateTimePicker(options=datepicker_opts))
    reef = forms.ModelChoiceField(required=False,
                                  queryset=Reef.objects.all())
    habitat = forms.ModelChoiceField(required=False,
                                     queryset=ReefType.objects.all())
    equipment = forms.ModelChoiceField(required=False,
                                       queryset=Equipment.objects.filter(set__in=Set.objects.all()).distinct())
    bait = forms.ModelChoiceField(required=False,
                                  queryset=Bait.objects.filter(set__in=Set.objects.all()).distinct())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline set-search form-group-sm'
        self.helper.form_method = "get"
        self.helper.layout = cfl.Layout(
            cfl.Fieldset(
                'Filter by:',
                'set_date',
                'reef',
                'habitat',
                'equipment',
                'bait'),
            cfl.Div(
                cfb.FormActions(
                    cfl.HTML("""<a role="button" class="btn btn-default cancel-button"
                    href="{% url "trip_set_list" trip_pk %}">Reset</a>"""),
                    cfl.Submit('', 'Search')),
                css_class='row pull-right'))


class EnvironmentMeasureForm(forms.ModelForm):
    dissolved_oxygen_measure = forms.ChoiceField(
        required=False,
        label='&nbsp;',
        choices=[('mgl', 'mg/L')]
    )

    class Meta:
        model = EnvironmentMeasure
        fields = ['water_temperature', 'salinity',
                  'conductivity', 'dissolved_oxygen', 'dissolved_oxygen_measure',
                  'tide_state', 'estimated_wind_speed', 'measured_wind_speed',
                  'wind_direction', 'cloud_cover', 'surface_chop']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.fields['measured_wind_speed'].label += '**'
        help_text = '<small class="help-block">**Use kts only when you have instrumentation ' \
                    'that makes a precise recording.</small>'
        self.helper.layout.append(cfl.Div(cfl.HTML(help_text)))


class ImageSelectWidget(forms.FileInput):
    def render(self, name, value, attrs=None):
        output = format_html('''
        <div class="image-select-widget" style="background-image:url({});">&nbsp;</div>
        <input type="hidden" value="{}" name="{}" />
        ''', static('images/upload_image.png') if not value else value, value, name)  # TODO need to get value URL
        return mark_safe(output)


class SetLevelDataForm(forms.ModelForm):
    bruv_image_url = forms.CharField(required=False,
                                     widget=ImageSelectWidget,
                                     label='Habitat photo: BRUV')
    splendor_image_url = forms.CharField(required=False,
                                         widget=ImageSelectWidget,
                                         label='Habitat photo: splendor of the reef')

    class Meta:
        model = Set
        fields = ['visibility', 'current_flow_instrumented', 'current_flow_estimated',
                  'bruv_image_url', 'splendor_image_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.fields['visibility'].required = False
        self.fields['visibility'].choices = \
            sorted(self.fields['visibility'].choices,
                   key=lambda _: _[0].isdigit() and int(_[0]) or _[0] == '' and -1 or 100)
        self.fields['visibility'].choices[0] = (None, '---')
        self.helper.layout = cfl.Layout(
            'visibility', 'current_flow_instrumented', 'current_flow_estimated',
            cfl.Div('bruv_image_url', 'splendor_image_url')
        )


class SelectizeWidget(forms.SelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<select class="selectize" multiple="multiple"{}>', flatatt(final_attrs))]
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output))


class SetLevelCommentsForm(forms.ModelForm):
    comments = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    message_to_annotators = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    tags = forms.MultipleChoiceField(widget=SelectizeWidget, choices=SetTag.get_choices, required=False)

    class Meta:
        model = Set
        fields = ['comments', 'message_to_annotators', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

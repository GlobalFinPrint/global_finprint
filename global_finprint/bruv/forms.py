from django import forms
from django.forms.utils import flatatt
from django.forms import ValidationError
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
from django.conf import settings


timepicker_opts = {"format": "HH:mm", "showClear": True}
datepicker_opts = {"format": "MMMM DD YYYY", "showClear": True, "extraFormats": ["D/M/Y"]}


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
        self.fields['latitude'].widget.attrs['step'] = 'any'
        self.fields['longitude'].widget.attrs['step'] = 'any'
        help_text = '<small class="help-block">*Required Field &nbsp;&nbsp;&nbsp; **Note: If code is left blank, ' \
                    'it will be automatically generated.</small>'
        self.helper.layout.append(cfl.Div(cfl.HTML(help_text)))


class SetSearchForm(forms.Form):
    search_set_date = forms.DateField(required=False,
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
    code = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        trip_id = kwargs.pop('trip_id', False)

        super().__init__(*args, **kwargs)

        if trip_id:
            self.fields['reef'].queryset = Reef.objects.filter(id__in=Trip.objects.get(pk=trip_id).
                                                               set_set.all().values('reef_habitat__reef'))

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline set-search form-group-sm'
        self.helper.form_method = "get"
        self.helper.layout = cfl.Layout(
            cfl.Div(
                'search_set_date',
                'reef',
                'habitat',
                'equipment',
                'bait',
                'code'),
            cfl.Div(
                cfb.FormActions(
                    cfl.HTML("""<a role="button" class="btn btn-default btn-fp cancel-button"
                    href="{% url "trip_set_list" trip_pk %}">Reset</a>"""),
                    cfl.Submit('', 'Search', css_class='btn-fp')),
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
    def __init__(self, image_url=None, attrs={}):
        self.image_url = image_url
        super().__init__(attrs)

    def render(self, name, value, attrs=None):
        template = '''
        <div class="image-select-widget-parent">
            <div class="image-select-widget" style="background-image:url({});">&nbsp;</div>
            <input type="file" value="{}" name="{}" />
            <div class="caption">{}</div>
        </div>
        '''
        output = format_html(template,
                             static('images/upload_image.png') if not self.image_url else self.image_url,
                             value,
                             name,
                             'Upload image' if not self.image_url else 'Choose another image')
        return mark_safe(output)


class SubstrateWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        template = '''
        <div class="habitat-substrate-parent clear">
            <div class="left clear">
                <div class="substrate-row">
                    <button class="btn btn-primary btn-fp add-substrate">+</button>
                    <span class="total">Total</span>
                </div>
            </div>

            <div class="center">
                <div class="substrate-row">
                    <div class="input-holder">
                        <input name="total-percent" type="number" readonly="readonly" value="0" />
                    </div>
                </div>
            </div>

            <div class="right">
                <div class="substrate-row">
                    <span class="help-text">Substrates must total 100%</span>
                </div>
            </div>
        </div>
        '''
        return mark_safe(format_html(template))


class SubstrateField(forms.Field):
    widget = SubstrateWidget

    def clean(self, value):
        pass

    def validate(self, value):
        super(SubstrateField, self).validate(value)
        if value != 100:  # check into json (?) for total %
            raise ValidationError('Substrate % must total 100', code='sumlessthan100')


class SetLevelDataForm(forms.ModelForm):
    bruv_image_file = forms.FileField(required=False,
                                      widget=ImageSelectWidget,
                                      label='Habitat photo: BRUV')
    splendor_image_file = forms.FileField(required=False,
                                          widget=ImageSelectWidget,
                                          label='Habitat photo: splendor of the reef')
    habitat_substrate = SubstrateField(required=False,
                                       label='Habitat substrate')

    class Meta:
        model = Set
        fields = ['visibility', 'current_flow_instrumented', 'current_flow_estimated',
                  'bruv_image_file', 'splendor_image_file', 'habitat_substrate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        s3_base_url = 'https://s3-us-west-2.amazonaws.com/' + settings.HABITAT_IMAGE_BUCKET
        bruv_image_url = s3_base_url + kwargs['instance'].bruv_image_url \
            if 'instance' in kwargs and kwargs['instance'] and kwargs['instance'].bruv_image_url else None
        splendor_image_url = s3_base_url + kwargs['instance'].splendor_image_url \
            if 'instance' in kwargs and kwargs['instance'] and kwargs['instance'].splendor_image_url else None
        self.fields['bruv_image_file'].widget = ImageSelectWidget(image_url=bruv_image_url)
        self.fields['splendor_image_file'].widget = ImageSelectWidget(image_url=splendor_image_url)
        self.fields['visibility'].required = False
        self.fields['visibility'].choices = \
            sorted(self.fields['visibility'].choices,
                   key=lambda _: _[0].isdigit() and int(_[0]) or _[0] == '' and -1 or 100)
        self.fields['visibility'].choices[0] = (None, '---')
        self.helper.layout = cfl.Layout(
            'visibility', 'current_flow_instrumented', 'current_flow_estimated',
            cfl.Div('bruv_image_file', 'splendor_image_file', 'habitat_substrate')
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

from django import forms
from django.db.models.functions import Lower
from django.forms.utils import flatatt
from django.forms import ValidationError
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse_lazy
from django.contrib.staticfiles.templatetags.staticfiles import static
from crispy_forms.helper import FormHelper
import crispy_forms.layout as cfl
import crispy_forms.bootstrap as cfb
from bootstrap3_datetime.widgets import DateTimePicker
from .models import Set, EnvironmentMeasure, Bait, Equipment, SetTag, BenthicCategory
from ..trip.models import Trip
from ..habitat.models import Reef, ReefType, Substrate, SubstrateComplexity
from django.conf import settings

US_WEST_AWS_S3 = 'https://s3-us-west-2.amazonaws.com/'

timepicker_opts = {"format": "HH:mm", "showClear": True}
datepicker_opts = {"format": "MMMM DD YYYY", "showClear": True, "extraFormats": ["D/M/Y"]}


class SetForm(forms.ModelForm):
    """
    Main set form
    """
    set_date = forms.DateField(
        input_formats=['%B %d %Y'],
        widget=DateTimePicker(options=datepicker_opts)
    )
    drop_time = forms.TimeField(
        input_formats=['%H:%M'],
        widget=DateTimePicker(options=timepicker_opts, icon_attrs={'class': 'glyphicon glyphicon-time'})
    )
    haul_date = forms.DateField(
        input_formats=['%B %d %Y'],
        widget=DateTimePicker(options=datepicker_opts),
        required=False
    )
    haul_time = forms.TimeField(
        input_formats=['%H:%M'],
        widget=DateTimePicker(options=timepicker_opts, icon_attrs={'class': 'glyphicon glyphicon-time'}),
        required=False
    )
    reef = forms.ModelChoiceField(
        queryset=Reef.objects.all()
    )
    habitat = forms.ModelChoiceField(
        queryset=ReefType.objects.all()
    )

    class Meta:
        model = Set
        fields = ['trip', 'set_date', 'haul_date', 'latitude', 'longitude', 'depth',
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
    """
    Set search form
    """
    search_set_date = forms.DateField(required=False,
                               input_formats=['%B %d %Y'],
                               widget=DateTimePicker(options=datepicker_opts))
    reef = forms.ModelChoiceField(required=False,
                                  queryset=Reef.objects.all().order_by(
                                      Lower('site__name'), Lower('name'), Lower('site__code'), Lower('code')
                                  ))
    habitat = forms.ModelChoiceField(required=False,
                                     queryset=ReefType.objects.all().order_by(Lower('type')))
    equipment = forms.ModelChoiceField(required=False,
                                       queryset=Equipment.objects.filter(set__in=Set.objects.all())
                                       .distinct().order_by(Lower('frame_type__type'), Lower('camera'), 'stereo')
                                       )
    bait = forms.ModelChoiceField(required=False,
                                  queryset=Bait.objects.filter(set__in=Set.objects.all())
                                  .distinct().order_by(Lower('type'), Lower('description'), 'oiled')
                                  )
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
    """
    Environmental measurement form used as part of set form; used twice in form for drop and haul
    """
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
    """
    Helper widget for image controls in set form
    """
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


class BenthicWidget(forms.Widget):
    """
    Helper widget for benthic category data in set form
    """
    def render(self, name, value, attrs=None):
        try:
            total_percent = value.pop('total_percent', 0)
            left = ''
            center = ''
            right = ''
            root_substrates = BenthicCategory.objects.all()

            for sp in list(zip(value['substrates'], value['percents'])):
                left += '''
                <div class="substrate-row">
                    <select class="substrate select form-control" name="benthic-category">
                '''
                for s in root_substrates:
                    left += '<option value="{}"{}>{}</option>'.format(
                        s.pk,
                        ' selected="selected"' if sp[0].pk == s.pk else '',
                        (s.get_level() * '-' + ' ') + s.name)
                left += '''
                    </select>
                </div>
                '''

                center += '''
                <div class="substrate-row"><div class="input-holder">
                    <input class="percent" name="percent" type="number" step="1" min="1" max="100" value="{}" />
                </div></div>
                '''.format(sp[1])

                right += '''
                <div class="substrate-row">
                    <a href="#" class="split">Split</a>
                    <a href="#" class="remove">Remove</a>
                </div>
                '''
        except (TypeError, AttributeError):
            total_percent = 0
            left = ''
            center = ''
            right = ''

        template = '''
        <div class="habitat-substrate-parent clear">
            <div class="left clear">
                {}
                <div class="substrate-row">
                    <button class="btn btn-primary btn-fp add-substrate">+</button>
                    <span class="total">Total</span>
                </div>
            </div>

            <div class="center">
                {}
                <div class="substrate-row">
                    <div class="input-holder">
                        <input name="total-percent" type="number" readonly="readonly" value="{}" />
                    </div>
                </div>
            </div>

            <div class="right">
                {}
                <div class="substrate-row">
                    <span class="help-text">Categories must total 100%</span>
                </div>
            </div>
        </div>
        '''
        return mark_safe(format_html(template, mark_safe(left), mark_safe(center), total_percent, mark_safe(right)))

    def value_from_datadict(self, data, files, name):
        return {
            'total_percent': int(data.get('total-percent')),
            'percents': [int(p) for p in data.getlist('percent')],
            'substrates': [int(s) for s in data.getlist('benthic-category')]
        }


class BenthicField(forms.Field):
    """
    Helper field for benthic data in set form
    """
    widget = BenthicWidget

    def to_python(self, value):
        if value is not None and 'substrates' in value and \
                len(value['substrates']) > 0 and isinstance(value['substrates'][0], int):
            value['substrates'] = [BenthicCategory.objects.get(pk=s_id) for s_id in value['substrates'][:]]
        return value

    def prepare_value(self, value):
        if hasattr(self, 'initial'):
            return self.initial

    def validate(self, value):
        super(BenthicField, self).validate(value)
        if value['total_percent'] != 100 and len(value['substrates']) > 0:
            raise ValidationError('Categories must total 100%', code='not_100')
        if len(value['substrates']) != len(set(value['substrates'])):
            raise ValidationError('Must not have duplicate categories', code='no_duplicates')


class SetLevelDataForm(forms.ModelForm):
    """
    Form for set level data used in set form
    """
    bruv_image_file = forms.FileField(required=False,
                                      widget=ImageSelectWidget,
                                      label='Habitat photo: BRUV')
    splendor_image_file = forms.FileField(required=False,
                                          widget=ImageSelectWidget,
                                          label='Habitat photo: splendor of the reef')
    benthic_category = BenthicField(required=False,
                                    label='Benthos Categories & Forms')
    substrate = forms.ModelChoiceField(required=False,
                                       queryset=Substrate.objects.all().order_by('type'))
    substrate_complexity = forms.ModelChoiceField(required=False,
                                                  queryset=SubstrateComplexity.objects.all().order_by('name'))

    class Meta:
        model = Set
        fields = ['visibility', 'current_flow_instrumented', 'current_flow_estimated',
                  'bruv_image_file', 'splendor_image_file', 'benthic_category',
                  'substrate', 'substrate_complexity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        s3_base_url = US_WEST_AWS_S3 + settings.HABITAT_IMAGE_BUCKET
        bruv_image_url = s3_base_url + kwargs['instance'].bruv_image_url \
            if 'instance' in kwargs and kwargs['instance'] and kwargs['instance'].bruv_image_url else None
        splendor_image_url = s3_base_url + kwargs['instance'].splendor_image_url \
            if 'instance' in kwargs and kwargs['instance'] and kwargs['instance'].splendor_image_url else None
        self.fields['bruv_image_file'].widget = ImageSelectWidget(image_url=bruv_image_url)
        self.fields['splendor_image_file'].widget = ImageSelectWidget(image_url=splendor_image_url)
        if 'instance' in kwargs and kwargs['instance'] and kwargs['instance'].benthiccategoryvalue_set:
            value = {
                'total_percent': 0,
                'percents': [],
                'substrates': []
            }
            for bcv in kwargs['instance'].benthiccategoryvalue_set.all():
                value['percents'].append(bcv.value)
                value['substrates'].append(bcv.benthic_category)
            value['total_percent'] = sum(value['percents'])
            self.fields['benthic_category'].initial = value
        self.fields['visibility'].required = False
        self.fields['visibility'].choices = \
            sorted(self.fields['visibility'].choices,
                   key=lambda _: _[0].isdigit() and int(_[0]) or _[0] == '' and -1 or 100)
        self.fields['visibility'].choices[0] = (None, '---')
        self.helper.layout = cfl.Layout(
            'visibility', 'current_flow_instrumented', 'current_flow_estimated',
            cfl.Div('bruv_image_file', 'splendor_image_file', 'benthic_category'),
            'substrate', 'substrate_complexity'
        )


class SelectizeWidget(forms.SelectMultiple):
    """
    Helper widget for selectize controls (autocomplete with multi-select)
    """
    template = '<select class="selectize" multiple="multiple"{}>'

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html(self.template, flatatt(final_attrs))]
        options = self.render_options(choices)
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe('\n'.join(output))


class SetLevelCommentsForm(forms.ModelForm):
    """
    Form for set level comments used in set form
    """
    comments = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    tags = forms.MultipleChoiceField(widget=SelectizeWidget, choices=SetTag.get_choices, required=False)

    class Meta:
        model = Set
        fields = ['comments','tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False


class SetBulkUploadForm(forms.Form):
    set_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        trip_id = kwargs.pop('trip_id')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('set_bulk_upload', args=[trip_id])
        self.helper.form_class = 'form-inline'
        self.helper.layout = cfl.Layout(
            cfl.Field('set_file', css_class='form-control'),
        )
        self.helper.add_input(cfl.Submit('upload', 'Upload', css_class='btn-fp'))

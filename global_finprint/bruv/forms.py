from django import forms
from crispy_forms.helper import FormHelper
import crispy_forms.layout as cfl
import crispy_forms.bootstrap as cfb
from bootstrap3_datetime.widgets import DateTimePicker
from .models import Set, EnvironmentMeasure, Bait, Equipment
from ..trip.models import Trip
from ..habitat.models import Reef, ReefType, ReefHabitat


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
        fields = ['trip', 'code', 'set_date', 'latitude', 'longitude', 'depth',
                  'drop_time', 'haul_time', 'reef', 'habitat', 'equipment', 'bait', 'visibility',
                  'reef_habitat',]
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

        self.fields['visibility'].choices = \
            sorted(self.fields['visibility'].choices,
                   key=lambda _: _[0].isdigit() and int(_[0]) or _[0] == '' and -1 or 100)
        self.fields['visibility'].choices[0] = (None, '---')

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.fields['code'].label += '**'
        self.helper.layout.append(
            cfl.HTML('<br>'))
        self.helper.layout.append(
            cfl.Div(
                cfl.HTML('<small class="help-block">**Note: If code is left blank, it will be automatically generated.</small>'),
                css_class='row pull-left'))


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
    class Meta:
        model = EnvironmentMeasure
        fields = ['water_temperature', 'salinity',
                  'conductivity', 'dissolved_oxygen', 'current_flow',
                  'current_direction', 'tide_state', 'estimated_wind_speed',
                  'wind_direction', 'cloud_cover', 'surface_chop']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

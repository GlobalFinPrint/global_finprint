from django import forms
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit, HTML
from ..core.models import Affiliation
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
    annotator = forms.ModelChoiceField(required=False,
                                       queryset=Annotator.objects.all(),
                                       label='Assigned annotator')
    affiliation = forms.ModelChoiceField(required=False,
                                         queryset=Affiliation.objects.all())
    number_assigned = forms.ChoiceField(required=False,
                                        choices=[(None, '----'), (0, 0), (1, 1), (2, 2), ('3+', '3+')])

    def __init__(self, *args, **kwargs):
        trip_id = kwargs.pop('trip_id')
        reset_url = reverse('video_annotator_list', kwargs={'trip_id': trip_id})
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline video-annotator-search'
        self.helper.form_action = reverse('video_annotator_list', kwargs={'trip_id': trip_id})
        self.helper.form_method = "get"
        self.helper.layout.append(
                FormActions(HTML("""<a role="button" class="btn btn-default cancel-button"
                href="{0}">Reset search</a>""".format(reset_url)), Submit('', 'Search videos')))


class VideoAnnotatorForm(forms.ModelForm):
    affiliation = forms.ModelChoiceField(queryset=Affiliation.objects.order_by('name'))
    annotators = forms.ModelMultipleChoiceField(queryset=Annotator.objects.order_by('user__last_name'))

    class Meta:
        model = VideoAnnotator
        fields = ['video', 'affiliation', 'annotators', 'assigned_by']
        widgets = {'assigned_by': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        trip_id = kwargs.pop('trip_id')
        reset_url = reverse('video_annotator_list', kwargs={'trip_id': trip_id})
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline video-annotator'
        self.helper.form_action = reverse('video_annotator_list', kwargs={'trip_id': trip_id})
        self.helper.layout.append(
                FormActions(HTML("""<a role="button" class="btn btn-default cancel-button"
                href="{0}">Cancel</a>""".format(reset_url)), Submit('save', 'Add annotators')))

    def save(self, *args, **kwargs):
        existing_ann = self.cleaned_data['video'].annotators_assigned()
        return list(
            VideoAnnotator(video=self.cleaned_data['video'],
                           annotator=ann,
                           assigned_by=self.cleaned_data['assigned_by']
                           ).save()
            for ann in self.cleaned_data['annotators']
            if ann not in existing_ann
        )


class SelectTripForm(forms.Form):
    trip = forms.ModelChoiceField(required=True, queryset=Trip.objects.all())
    affiliation = forms.ModelChoiceField(required=False,
                                         queryset=Affiliation.objects.all(),
                                         help_text='Required for auto assign')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline video-annotator-trip-select'
        self.helper.layout.append(
                FormActions(
                        HTML("""<a role="button" class="btn btn-info manual-assign"
                        href="#">Manual assign</a>"""),
                        HTML("""<a role="button" class="btn btn-primary auto-assign"
                        href="#">Auto assign</a>""")
                ))

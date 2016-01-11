from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Count
from ..models import VideoAnnotator, Video, Lead
from ..forms import VideoAnnotatorForm, VideoAnnotatorSearchForm


class VideoAnnotatorListView(LoginRequiredMixin, CreateView):
    model = VideoAnnotator
    form_class = VideoAnnotatorForm
    context_object_name = 'video_annotator'
    template_name = 'pages/annotation/video_annotator_list.html'
    success_msg = 'Video annotator assigned'
    success_url = reverse_lazy('video_annotator_list')

    def form_invalid(self, form):
        messages.error(self.request, 'Form errors found')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            if not self.request.user.is_authenticated():
                raise Lead.DoesNotExist

            initial = {'assigned_by': Lead.objects.get(user_id=self.request.user)}
            if 'video' in self.request.GET:
                initial['video'] = get_object_or_404(Video, pk=self.request.GET.get('video', 0))
            context['form'] = VideoAnnotatorForm(initial=initial)

        except Lead.DoesNotExist:
            context['form'] = None

        context['search_form'] = VideoAnnotatorSearchForm(self.request.GET)
        if self.request.GET and context['search_form'].is_valid():
            search_values = context['search_form'].cleaned_data
            query = Video.objects
            if search_values['trip'] is not None:
                query = query.filter(set__trip=search_values['trip'])
            if search_values['team'] is not None:
                query = query.filter(set__trip__team=search_values['team'])
            if search_values['location'] is not None:
                query = query.filter(set__trip__location=search_values['location'])
            if search_values['region'] is not None:
                query = query.filter(set__trip__region=search_values['region'])
            if search_values['annotator'] is not None:
                query = query.filter(videoannotator__annotator=search_values['annotator'])
            if search_values['number_assigned'] not in (None, ''):
                query = query.annotate(Count('videoannotator'))
                if search_values['number_assigned'] == '3+':
                    query = query.filter(videoannotator__count__gte=3)
                else:
                    query = query.filter(videoannotator__count=search_values['number_assigned'])
            context['videos'] = query.all()
        else:
            context['videos'] = Video.objects.all()
        return context

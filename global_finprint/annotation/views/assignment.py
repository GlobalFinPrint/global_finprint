from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Count
from django.http.response import HttpResponseForbidden, HttpResponseNotFound, \
    HttpResponse, JsonResponse, HttpResponseRedirect
from ...bruv.models import Trip
from ..models import VideoAnnotator, Video, Lead, Annotator
from ..forms import VideoAnnotatorForm, VideoAnnotatorSearchForm, SelectTripForm


class VideoAnnotatorSelectTripView(LoginRequiredMixin, View):
    template = 'pages/annotation/video_annotator_select_trip.html'

    def get(self, request):
        context = {'select_trip_form': SelectTripForm}
        return render_to_response(self.template, context=context)


class VideoAnnotatorListView(LoginRequiredMixin, CreateView):
    model = VideoAnnotator
    form_class = VideoAnnotatorForm
    context_object_name = 'video_annotator'
    template_name = 'pages/annotation/video_annotator_list.html'
    success_msg = 'Video annotator assigned'

    def get_success_url(self):
        return reverse_lazy('video_annotator_list', kwargs={'trip_id': self.kwargs['trip_id']})

    def get_form_kwargs(self):
        return {'trip_id': self.kwargs['trip_id']}

    def form_invalid(self, form):
        messages.error(self.request, 'Form errors found')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['trip_name'] = str(get_object_or_404(Trip, pk=self.kwargs['trip_id']))
        try:
            if not self.request.user.is_authenticated():
                raise Lead.DoesNotExist

            initial = {'assigned_by': Lead.objects.get(user_id=self.request.user)}
            if 'video' in self.request.GET:
                initial['video'] = get_object_or_404(Video, pk=self.request.GET.get('video', 0))
            context['form'] = VideoAnnotatorForm(initial=initial, trip_id=self.kwargs['trip_id'])
            context['is_lead'] = True

        except Lead.DoesNotExist:
            context['form'] = None
            context['is_lead'] = False

        context['search_form'] = VideoAnnotatorSearchForm(self.request.GET, trip_id=(self.kwargs['trip_id']))
        if self.request.GET and context['search_form'].is_valid():
            search_values = context['search_form'].cleaned_data
            query = Video.objects.filter(set__trip=self.kwargs['trip_id'])
            if search_values['team'] is not None:
                query = query.filter(set__trip__team=search_values['team'])
            if search_values['location'] is not None:
                query = query.filter(set__trip__location=search_values['location'])
            if search_values['region'] is not None:
                query = query.filter(set__trip__location__region=search_values['region'])
            if search_values['annotator'] is not None:
                query = query.filter(videoannotator__annotator=search_values['annotator'])
            if search_values['affiliation'] is not None:
                query = query.filter(videoannotator__annotator__affiliation=search_values['affiliation'])
            if search_values['number_assigned'] not in (None, ''):
                query = query.annotate(Count('videoannotator'))
                if search_values['number_assigned'] == '3+':
                    query = query.filter(videoannotator__count__gte=3)
                else:
                    query = query.filter(videoannotator__count=search_values['number_assigned'])
            context['videos'] = query.distinct().order_by('pk')
        else:
            context['videos'] = Video.objects.filter(set__trip=self.kwargs['trip_id']).order_by('pk')
        return context


class RemoveVideoAnnotatorView(View):
    def post(self, request):
        try:
            Lead.objects.get(user=request.user)
        except Lead.DoesNotExist:
            return HttpResponseForbidden()

        va = get_object_or_404(VideoAnnotator, pk=request.POST.get('id'))

        if va.status != 'N':
            return HttpResponseNotFound()

        va.delete()

        return HttpResponse('ok')


class DisableVideoAnnotatorView(View):
    def post(self, request):
        try:
            Lead.objects.get(user=request.user)
        except Lead.DoesNotExist:
            return HttpResponseForbidden()

        va = get_object_or_404(VideoAnnotator, pk=request.POST.get('id'))
        va.status = 'D'
        va.save()

        return HttpResponse('ok')


class EnableVideoAnnotatorView(View):
    def post(self, request):
        try:
            Lead.objects.get(user=request.user)
        except Lead.DoesNotExist:
            return HttpResponseForbidden()

        va = get_object_or_404(VideoAnnotator, pk=request.POST.get('id'))
        va.status = 'I'
        va.save()

        return HttpResponse('ok')


class VideoAnnotatorJSONListView(View):
    def get(self, request):
        annotators = Annotator.objects.all()
        if request.GET.get('affiliation', None):
            annotators = annotators.filter(affiliation=request.GET['affiliation'])
        return JsonResponse({'annotators': list({'id': a.id, 'user': str(a)} for a in annotators)})


class VideoAutoAssignView(View):
    def get(self, request, ids):
        trip_id, aff_id = ids.split('_')
        try:
            videos = Video.objects.filter(set__trip_id=trip_id).all()
            annotators = Annotator.objects.filter(affiliation_id=aff_id).all()
            messages.success(request, 'Videos auto assigned!')
        except Exception:  # TODO need to be more specific
            messages.error(request, 'Error auto assigning videos')
        return HttpResponseRedirect(reverse_lazy('video_annotator_list', kwargs={'trip_id': trip_id}))

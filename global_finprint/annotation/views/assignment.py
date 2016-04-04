from django.views.generic import CreateView, View
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Count
from django.http.response import HttpResponseForbidden, HttpResponseNotFound, \
    HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import RequestContext
from ...trip.models import Trip
from ...bruv.models import Set
from ...habitat.models import Location
from ...core.mixins import UserAllowedMixin
from ..models import VideoAnnotator, Video, Lead, Annotator, Observation, AnnotationState
from ...core.models import Affiliation
from ..forms import VideoAnnotatorForm, VideoAnnotatorSearchForm, SelectTripForm


class VideoAnnotatorSelectTripView(UserAllowedMixin, View):
    template = 'pages/annotation/video_annotator_select_trip.html'

    def get(self, request):
        context = RequestContext(request, {'select_trip_form': SelectTripForm})
        return render_to_response(self.template, context=context)


class VideoAnnotatorListView(UserAllowedMixin, CreateView):
    model = VideoAnnotator
    form_class = VideoAnnotatorForm
    context_object_name = 'video_annotator'
    template_name = 'pages/annotation/video_annotator_list.html'
    success_msg = 'Annotator(s) added'

    def get_success_url(self):
        messages.success(self.request, self.success_msg)
        return reverse_lazy('video_annotator_list', kwargs={'trip_id': self.kwargs['trip_id']})

    def get_form(self, **kwargs):
        return self.form_class(self.request.POST or None, trip_id=self.kwargs['trip_id'])

    def form_invalid(self, form):
        errors = ' ,'.join(list(str(e) for e in form.errors.items() + form.non_field_errors()))
        messages.error(self.request, 'Form errors found: {}'.format(errors))
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

        context['assignments'] = VideoAnnotator.objects.filter(video__set__trip=self.kwargs['trip_id']).order_by('pk')

        context['search_form'] = VideoAnnotatorSearchForm(self.request.GET, trip_id=(self.kwargs['trip_id']))
        if self.request.GET and context['search_form'].is_valid():
            search_values = context['search_form'].cleaned_data
            query = Video.objects.filter(set__trip=self.kwargs['trip_id'])
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


class RemoveVideoAnnotatorView(UserAllowedMixin, View):
    def post(self, request):
        try:
            Lead.objects.get(user=request.user)
        except Lead.DoesNotExist:
            return HttpResponseForbidden()

        va = get_object_or_404(VideoAnnotator, pk=request.POST.get('id'))

        if va.status_id != 1:
            return HttpResponseNotFound()

        va.delete()

        return HttpResponse('ok')


class DisableVideoAnnotatorView(UserAllowedMixin, View):
    def post(self, request):
        try:
            Lead.objects.get(user=request.user)
        except Lead.DoesNotExist:
            return HttpResponseForbidden()

        va = get_object_or_404(VideoAnnotator, pk=request.POST.get('id'))
        va.status_id = 5
        va.save()

        return HttpResponse('ok')


class EnableVideoAnnotatorView(UserAllowedMixin, View):
    def post(self, request):
        try:
            Lead.objects.get(user=request.user)
        except Lead.DoesNotExist:
            return HttpResponseForbidden()

        va = get_object_or_404(VideoAnnotator, pk=request.POST.get('id'))
        va.status_id = 2
        va.save()

        return HttpResponse('ok')


class VideoAnnotatorJSONListView(UserAllowedMixin, View):
    def get(self, request):
        annotators = []
        selected_annotators = []

        if request.GET.get('video', None):
            selected_annotators = Annotator.objects.filter(videoannotator__video_id=request.GET['video'])
        if request.GET.get('affiliation', None):
            annotators = Annotator.objects.filter(affiliation_id=request.GET['affiliation']) \
                .order_by('user__last_name')

        return JsonResponse({'annotators': list({'id': a.id, 'user': str(a)} for a
                                                in annotators if a not in selected_annotators)})


class VideoAutoAssignView(UserAllowedMixin, View):
    def assign_video(self, annotators, video):
        avail = list(a for a in annotators if video not in a.videos_assigned())
        assigned_by = Lead.objects.get(user_id=self.request.user)
        while len(video.annotators_assigned()) < 2 and len(annotators) > 1:
            ann = min(avail, key=lambda a: len(a.videos_assigned()))
            VideoAnnotator(annotator=ann, video=video, assigned_by=assigned_by).save()
            avail.remove(ann)

    def get(self, request, ids):
        trip_id, aff_id = ids.split('_')
        annotators = Annotator.objects.filter(affiliation_id=aff_id).all()
        try:
            for video in Video.objects.filter(set__trip_id=trip_id).all():
                self.assign_video(annotators, video)
            messages.success(request, 'Videos auto assigned!')

        except Lead.DoesNotExist:
            messages.error(request, 'Logged in user must be a Lead to assign videos')
        except Exception as e:  # TODO need to be more specific (?)
            messages.error(request, 'Error auto assigning videos: {}'.format(e))

        return HttpResponseRedirect(reverse_lazy('video_annotator_list', kwargs={'trip_id': trip_id}))


class AssignmentListView(UserAllowedMixin, View):
    template_name = 'pages/annotation/assignment_list.html'

    def get(self, request):
        context = RequestContext(request, {
            'locations': Location.objects.order_by('name').all(),
            'trips': Trip.objects.order_by('start_date').all(),
            'affils': Affiliation.objects.order_by('name').all(),
            'statuses': AnnotationState.objects.all()
        })
        return render_to_response(self.template_name, context=context)


class AssignmentListTbodyView(UserAllowedMixin, View):
    template_name = 'pages/annotation/assignment_list_tbody.html'

    def post(self, request):
        query = VideoAnnotator.objects.all()
        unassigned = Set.objects.annotate(Count('video__videoannotator')) \
                                .filter(video__videoannotator__count=0)

        trips = request.POST.getlist('trip[]')
        sets = request.POST.getlist('set[]')
        annos = request.POST.getlist('anno[]')

        if trips:
            query = query.filter(video__set__trip_id__in=(int(t) for t in trips))
            unassigned = unassigned.filter(trip_id__in=(int(t) for t in trips))

        if sets:
            query = query.filter(video__set__id__in=(int(s) for s in sets))
            unassigned = unassigned.filter(set_id__in=(int(s) for s in sets))

        if annos:
            query = query.filter(annotator_id__in=(int(a) for a in annos))
            unassigned = []

        context = RequestContext(request, {'assignments': query, 'unassigned': unassigned})
        return render_to_response(self.template_name, context=context)


class AssignmentModalBodyView(UserAllowedMixin, View):
    template_name = 'pages/annotation/assignment_modal_body.html'

    def get(self, request, set_id):
        set = Set.objects.get(id=set_id)
        current_assignments = set.video.videoannotator_set.all()
        context = RequestContext(request, {
            'set': set,
            'current': current_assignments,
            'current_annos': [a.annotator for a in current_assignments],
            'affiliations': Affiliation.objects.order_by('name').all()
        })
        return render_to_response(self.template_name, context=context)


class AssignmentManageView(UserAllowedMixin, View):
    template_name = 'pages/annotation/assignment_manage.html'

    def get(self, request, assignment_id):
        context = RequestContext(request, {
            'assignment': VideoAnnotator.objects.get(id=assignment_id),
            'observations': Observation.objects.filter(video_annotator_id=assignment_id)
        })
        return render_to_response(self.template_name, context=context)

    def post(self, request):
        pass

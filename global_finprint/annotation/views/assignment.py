from django.views.generic import View
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Count
from django.http.response import JsonResponse, HttpResponseRedirect
from django.template import RequestContext
from ...trip.models import Trip
from ...bruv.models import Set
from ...habitat.models import Location
from ...core.mixins import UserAllowedMixin
from ..models import VideoAnnotator, Video, Lead, Annotator, Observation, AnnotationState
from ...core.models import Affiliation


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
        status = request.POST.getlist('status[]')
        assigned = request.POST.get('assigned')

        if trips:
            query = query.filter(video__set__trip_id__in=(int(t) for t in trips))
            unassigned = unassigned.filter(trip_id__in=(int(t) for t in trips))

        if sets:
            query = query.filter(video__set__id__in=(int(s) for s in sets))
            unassigned = unassigned.filter(id__in=(int(s) for s in sets))

        if annos:
            query = query.filter(annotator_id__in=(int(a) for a in annos))
            unassigned = []

        if status:
            query = query.filter(status_id__in=(int(s) for s in status))
            unassigned = []

        if assigned != '':
            if assigned == '5+':
                query = query.annotate(Count('video__videoannotator')).filter(video__videoannotator__gte=5)
                unassigned = []
            elif int(assigned) == 0:
                query = []
            else:
                query = query.annotate(Count('video__videoannotator')) \
                    .filter(video__videoannotator__count=int(assigned))
                unassigned = []

        context = RequestContext(request, {'assignments': query, 'unassigned': unassigned})
        return render_to_response(self.template_name, context=context)


class AssignmentModalBodyView(UserAllowedMixin, View):
    template_name = 'pages/annotation/assignment_modal_body.html'

    def get(self, request, set_id):
        set = get_object_or_404(Set, id=set_id)
        current_assignments = set.video.videoannotator_set.all()
        context = RequestContext(request, {
            'set': set,
            'current': current_assignments,
            'current_annos': [a.annotator for a in current_assignments],
            'affiliations': Affiliation.objects.order_by('name').all()
        })
        return render_to_response(self.template_name, context=context)

    def post(self, request, set_id):
        set = get_object_or_404(Set, id=set_id)
        for anno_id in request.POST.getlist('anno[]'):
            VideoAnnotator(
                annotator=Annotator.objects.get(id=anno_id),
                video=set.video,
                assigned_by=Lead.objects.get(user_id=request.user),
            ).save()
        return JsonResponse({'status': 'ok'})


class AssignmentManageView(UserAllowedMixin, View):
    template_name = 'pages/annotation/assignment_manage.html'

    def get(self, request, assignment_id):
        context = RequestContext(request, {
            'assignment': get_object_or_404(VideoAnnotator, id=assignment_id),
            'observations': Observation.objects.filter(video_annotator_id=assignment_id)
        })
        return render_to_response(self.template_name, context=context)

    def post(self, request, assignment_id):
        action = request.POST.get('action')
        new_state = request.POST.get('new')
        assignment = get_object_or_404(VideoAnnotator, id=assignment_id)

        if action == 'delete' and assignment.status_id == 1:
            assignment.delete()
        elif action == 'update' and new_state is not None:
            assignment.status_id = int(new_state)
            assignment.save()

        return JsonResponse({'status': 'ok'})

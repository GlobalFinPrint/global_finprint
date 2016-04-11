from django.views.generic import View
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Count
from django.http.response import JsonResponse
from django.template import RequestContext
from ...trip.models import Trip
from ...bruv.models import Set
from ...habitat.models import Location
from ...core.mixins import UserAllowedMixin
from ..models import Assignment, Video, Observation, AnnotationState
from ...core.models import Affiliation, FinprintUser


class VideoAutoAssignView(UserAllowedMixin, View):
    def assign_video(self, annotators, video, num):
        avail = list(a for a in annotators if video not in a.active_assignments())
        assigned_by = FinprintUser.objects.get(user_id=self.request.user)
        while len(video.annotators_assigned()) < num and len(annotators) > 0 and len(avail) > 0:
            ann = min(avail, key=lambda a: len(a.active_assignments()))
            Assignment(annotator=ann, video=video, assigned_by=assigned_by).save()
            avail.remove(ann)

    def post(self, request):
        trip_id = request.POST.get('trip')
        aff_id = request.POST.get('affiliation')
        num = int(request.POST.get('num'))

        annotators = FinprintUser.objects.filter(affiliation_id=aff_id).all()
        for video in Video.objects.filter(set__trip_id=trip_id).all():
            self.assign_video(annotators, video, num)

        return JsonResponse({'status': 'ok'})


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
        query = Assignment.objects.all()
        unassigned = Set.objects.annotate(Count('video__assignment')) \
                                .filter(video__assignment__count=0)

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
                query = query.annotate(Count('video__assignment')).filter(video__assignment__gte=5)
                unassigned = []
            elif int(assigned) == 0:
                query = []
            else:
                query = query.annotate(Count('video__assignment')) \
                    .filter(video__assignment__count=int(assigned))
                unassigned = []

        context = RequestContext(request, {'assignments': query, 'unassigned': unassigned})
        return render_to_response(self.template_name, context=context)


class AssignmentModalBodyView(UserAllowedMixin, View):
    template_name = 'pages/annotation/assignment_modal_body.html'

    def get(self, request, set_id):
        set = get_object_or_404(Set, id=set_id)
        current_assignments = set.video.assignment_set.all()
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
            Assignment(
                annotator=FinprintUser.objects.get(id=anno_id),
                video=set.video,
                assigned_by=FinprintUser.objects.get(user_id=request.user),
            ).save()
        return JsonResponse({'status': 'ok'})


class AssignmentManageView(UserAllowedMixin, View):
    template_name = 'pages/annotation/assignment_manage.html'

    def get(self, request, assignment_id):
        context = RequestContext(request, {
            'assignment': get_object_or_404(Assignment, id=assignment_id),
            'observations': Observation.objects.filter(assignment_id=assignment_id)
        })
        return render_to_response(self.template_name, context=context)

    def post(self, request, assignment_id):
        action = request.POST.get('action')
        new_state = request.POST.get('new')
        assignment = get_object_or_404(Assignment, id=assignment_id)

        if action == 'delete' and assignment.status_id == 1:
            assignment.delete()
        elif action == 'update' and new_state is not None:
            assignment.status_id = int(new_state)
            assignment.save()

        return JsonResponse({'status': 'ok'})

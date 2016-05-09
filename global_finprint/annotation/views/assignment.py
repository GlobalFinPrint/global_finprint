from django.views.generic import View
from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Count
from django.http.response import JsonResponse
from django.template import RequestContext
from ...core.mixins import UserAllowedMixin
from ...trip.models import Trip
from ...bruv.models import Set
from ...habitat.models import Location
from ...core.models import Affiliation, FinprintUser
from ..models.video import Assignment, Video, AnnotationState
from datetime import date, timedelta


class VideoAutoAssignView(UserAllowedMixin, View):
    def assign_video(self, annotators, video, num):
        avail = list(a for a in annotators if a not in video.annotators_assigned())
        assigned_by = FinprintUser.objects.get(user=self.request.user)
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
        assigned_ago = request.POST.get('assigned-ago')

        if trips:
            query = query.filter(video__set__trip_id__in=(int(t) for t in trips))
            unassigned = unassigned.filter(trip_id__in=(int(t) for t in trips))

        if sets:
            query = query.filter(video__set__id__in=(int(s) for s in sets))
            unassigned = unassigned.filter(id__in=(int(s) for s in sets))

        if annos:
            query = query.filter(annotator_id__in=(int(a) for a in annos))
            unassigned = unassigned.none()

        if status:
            query = query.filter(status_id__in=(int(s) for s in status))
            unassigned = unassigned.none()

        if assigned != '':
            if assigned == '5+':
                query = query.annotate(Count('video__assignment')).filter(video__assignment__count__gte=5)
                unassigned = unassigned.none()
            elif int(assigned) == 0:
                query = query.none()
            else:
                query = query.annotate(Count('video__assignment')) \
                    .filter(video__assignment__count=int(assigned))
                unassigned = unassigned.none()

        if assigned_ago != '':
            try:
                query = query.filter(create_datetime__gte=(date.today() - timedelta(days=int(assigned_ago))))
                unassigned = unassigned.none()
            except ValueError:
                pass

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
        assignment = get_object_or_404(Assignment, id=assignment_id)
        context = RequestContext(request, {
            'assignment': assignment,
            'trip': assignment.video.set.trip,
            'set': assignment.video.set,
            'observations': assignment.observation_set.all(),
            'for': ' for {0} by {1}'.format(assignment.video.set, assignment.annotator)
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

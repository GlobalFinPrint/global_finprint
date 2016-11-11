from datetime import date, timedelta

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
from ..models.project import Project


class VideoAutoAssignView(UserAllowedMixin, View):
    def assign_video(self, annotators, video, num, project):
        avail = list(a for a in annotators if a not in video.annotators_assigned())
        assigned_by = FinprintUser.objects.get(user=self.request.user)
        assign_count = 0
        while len(video.annotators_assigned()) < num and len(annotators) > 0 and len(avail) > 0:
            ann = min(avail, key=lambda a: len(a.active_assignments()))
            Assignment(annotator=ann, video=video, assigned_by=assigned_by, project=project).save()
            avail.remove(ann)
            assign_count += 1
        return assign_count

    def post(self, request):
        trip_id = request.POST.get('trip')
        aff_id = request.POST.get('affiliation')
        num = int(request.POST.get('num'))
        include_leads = bool(request.POST.get('include_leads', False))
        project = get_object_or_404(Project, id=request.POST.get('project'))

        annotators = FinprintUser.objects.filter(affiliation_id=aff_id).all()
        if not include_leads:
            annotators = list(a for a in annotators if not a.is_lead())
        video_count = 0
        assigned_count = 0
        new_count = 0
        for video in Video.objects.filter(set__trip_id=trip_id).exclude(file__isnull=True).exclude(file='').all():
            video_count += 1
            new_count += self.assign_video(annotators, video, num, project)
            assigned_count += len(video.annotators_assigned())

        return JsonResponse(
            {
                'status': 'ok',
                'video_count': video_count,
                'assignments':
                {
                    'total': video_count * num,
                    'assigned': assigned_count,
                    'newly_assigned': new_count
                }
            }
        )


class AssignmentListView(UserAllowedMixin, View):
    template_name = 'pages/annotation/assignment_list.html'

    def get(self, request):
        context = RequestContext(request, {
            'locations': Location.objects.order_by('name').all().prefetch_related('trip_set'),
            'trips': Trip.objects.order_by('start_date').all().prefetch_related('set_set'),
            'affils': Affiliation.objects.order_by('name').all().prefetch_related('finprintuser_set'),
            'statuses': AnnotationState.objects.all(),
            'projects': Project.objects.order_by('id').all()
        })
        return render_to_response(self.template_name, context=context)


class AssignmentListTbodyView(UserAllowedMixin, View):
    template_name = 'pages/annotation/assignment_list_tbody.html'

    def post(self, request):
        selected_related = [
            'video', 'video__set', 'video__set__trip', 'annotator', 'annotator__user'
        ]
        query = Assignment.objects.all().select_related(*selected_related).prefetch_related('observation_set')
        unassigned = Set.objects.annotate(Count('video__assignment')) \
                                .filter(video__assignment__count=0) \
                                .exclude(video__file__isnull=True).exclude(video__file='')

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

        context = RequestContext(request, {'assignments': sorted(query, key=lambda a: str(a.set())),
                                           'unassigned': sorted(unassigned, key=lambda s: str(s))
                                           })
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
            'affiliations': Affiliation.objects.order_by('name').all(),
            'projects': Project.objects.order_by('id').all()
        })
        return render_to_response(self.template_name, context=context)

    def post(self, request, set_id):
        set = get_object_or_404(Set, id=set_id)
        project = get_object_or_404(Project, id=request.POST.get('project'))
        for anno_id in request.POST.getlist('anno[]'):
            Assignment(
                annotator=FinprintUser.objects.get(id=anno_id),
                video=set.video,
                assigned_by=FinprintUser.objects.get(user_id=request.user),
                project=project
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
            'observations': assignment.observation_set.all()
                                 .select_related('animalobservation__animal',
                                                 'assignment__annotator__user',
                                                 'assignment__annotator__affiliation',
                                                 'assignment__video__set__trip',)
                                 .prefetch_related('event_set', 'event_set__attribute'),
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

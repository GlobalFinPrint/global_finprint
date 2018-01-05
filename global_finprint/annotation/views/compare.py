from django.views.generic import View
from django.template import Context
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from global_finprint.core.mixins import UserAllowedMixin
from global_finprint.bruv.models import Set
from global_finprint.annotation.models.video import Assignment, Project
from global_finprint.annotation.models.observation import MasterRecord, MasterRecordState
from global_finprint.annotation.models.animal import AnimalGroup


class AssignmentCompareView(UserAllowedMixin, View):
    """
    View for the assignment compare (timelines) screen found at /assignment/compare/<set_id>?project=<project_id>
    """
    template_name = 'pages/annotation/assignment_compare.html'

    def get(self, request, set_id):
        set = get_object_or_404(Set, pk=set_id)
        project = get_object_or_404(Project, pk=request.GET.get('project', 1))
        animal_groups = AnimalGroup.project_groups(project)
        # default to master status 'in progress':
        master_status = get_object_or_404(MasterRecordState, pk=1)
        master, created = MasterRecord.objects.get_or_create(
            set=set, project=project, defaults={'status': master_status})
        context = Context({
            'trip': set.trip,
            'set': set,
            'video_length': set.video.length(),
            'master': master,
            'project': project,
            'animal_groups': animal_groups,
            # exclude assignments that are 'rejected' or 'disabled':
            'assignment_set': set.video.assignment_set.exclude(status__in=[5, 6]).filter(project=project),
            'state_list': MasterRecordState.objects.all(),
            'anonymous': settings.HIDE_COMPARE_ANNOTATORS if settings.HIDE_COMPARE_ANNOTATORS else False
        })
        return render(request, self.template_name, context=context)


class AssignmentDetailView(UserAllowedMixin, View):
    """
    Endpoint for assignment detail for the compare screen
    """
    def get(self, _, assignment_id):
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        observations = assignment.observation_set.all() \
            .prefetch_related('event_set',
                              'event_set__attribute') \
            .select_related('animalobservation',
                            'animalobservation__animal',
                            'assignment',
                            'assignment__annotator',
                            'assignment__annotator__user')
        observations = sorted(observations, key=lambda x: x.initial_observation_time())
        return JsonResponse({
            'observations': list(o.to_json(for_web=True) for o in observations)
        })


class GetMasterView(UserAllowedMixin, View):
    """
    Endpoints to get/update a master record for a given set
    """
    def get(self, request, set_id):
        project = get_object_or_404(Project, pk=request.GET.get('project', 1))
        master = get_object_or_404(MasterRecord, project=project, set=get_object_or_404(Set, pk=set_id))
        observations = master.masterobservation_set.all() \
            .prefetch_related('masterevent_set',
                              'masterevent_set__attribute') \
            .select_related('masteranimalobservation',
                            'masteranimalobservation__animal')
        observations = sorted(observations, key=lambda x: x.initial_observation_time())
        return JsonResponse({
            'observations': list(o.to_json(for_web=True) for o in observations)
        })

    def post(self, request, set_id):
        project = get_object_or_404(Project, pk=request.POST.get('project', 1))
        master_record = get_object_or_404(MasterRecord, project=project, set=get_object_or_404(Set, pk=set_id))
        original_observation_ids = list(int(org_obs_id) for org_obs_id in request.POST.getlist('original_observation_ids[]'))

        if set(original_observation_ids) == set(obs.id for obs in master_record.original_observations()):
            return JsonResponse({'success': 'no changes'})

        success, err_msg = master_record.copy_observations(original_observation_ids)
        if success:
            response = JsonResponse({'success': 'ok'})
        else:
            response = JsonResponse({'error': err_msg})
            response.status_code = 500
        return response

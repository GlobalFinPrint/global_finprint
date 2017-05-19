from django.views.generic import View
from django.template import Context
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from global_finprint.core.mixins import UserAllowedMixin
from global_finprint.trip.models import Trip
from global_finprint.bruv.models import Set
from global_finprint.annotation.models.video import Assignment, Project
from global_finprint.annotation.models.observation import MasterRecord, MasterRecordState


class AssignmentCompareView(UserAllowedMixin, View):
    """
    View for the assignment compare (timelines) screen found at /assignment/compare/<set_id>?project=<project_id>
    """
    template_name = 'pages/annotation/assignment_compare.html'

    def get(self, request, set_id):
        set = get_object_or_404(Set, pk=set_id)
        project = get_object_or_404(Project, pk=request.GET.get('project', 1))
        master_status = get_object_or_404(MasterRecordState, pk=1)
        master, created = MasterRecord.objects.get_or_create(set=set, project=project, status=master_status)
        context = Context({
            'set': set,
            'video_length': set.video.length(),
            'master': master,
            'project': project,
            'assignment_set': set.video.assignment_set.filter(project=project)
        })
        return render(request, self.template_name, context=context)


class MasterReviewView(UserAllowedMixin, View):
    """
    View for master record review screen found at /assignment/review/<master_record_id>
    """
    template_name = 'pages/annotation/master_review.html'

    def get(self, request, master_id):
        master_record = get_object_or_404(MasterRecord, pk=master_id)
        context = Context({
            'state_list': MasterRecordState.objects.all(),
            'master': master_record,
            'trip': master_record.set.trip,
            'set': master_record.set,
            'master_observations': sorted(master_record.masterobservation_set.all(),
                                          key=lambda o: o.initial_observation_time(),
                                          reverse=True),
            'for': ' for {}'.format(master_record.set)
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
        return JsonResponse(master.to_json())

    def post(self, request, set_id):
        project = get_object_or_404(Project, pk=request.POST.get('project', 1))
        master_record = get_object_or_404(MasterRecord, project=project, set=get_object_or_404(Set, pk=set_id))
        observation_ids = list(int(obs_id) for obs_id in request.POST.getlist('observation_ids[]'))

        if set(observation_ids) == set(obs.id for obs in master_record.original_observations()):
            return JsonResponse({'success': 'no changes'})

        success, err_msg = master_record.copy_observations(observation_ids)
        if success:
            response = JsonResponse({'success': 'ok'})
        else:
            response = JsonResponse({'error': err_msg})
            response.status_code = 500
        return response


class MasterSetCompleted(UserAllowedMixin, View):
    """
    Endpoint to mark a master record as 'completed'
    """
    def get(self, request, master_id):
        master = get_object_or_404(MasterRecord, pk=master_id)
        master.completed = (request.GET.get('checked', 'false') == 'true')
        master.save()
        return JsonResponse({'success': 'ok'})


class MasterSetDeprecated(UserAllowedMixin, View):
    """
    Endpoint to mark a master record as 'deprecated'
    """
    def get(self, request, master_id):
        master = get_object_or_404(MasterRecord, pk=master_id)
        master.deprecated = (request.GET.get('checked', 'false') == 'true')
        master.save()
        return JsonResponse({'success': 'ok'})


class MasterManageView(UserAllowedMixin, View):
    """
    Endpoint to update master record status
    """
    def post(self, request, master_id):
        master = get_object_or_404(MasterRecord, pk=master_id)
        return JsonResponse({'status': 'ok'})

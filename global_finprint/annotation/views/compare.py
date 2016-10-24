from django.views.generic import View
from django.template import RequestContext
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render_to_response
from global_finprint.core.mixins import UserAllowedMixin
from global_finprint.bruv.models import Set
from global_finprint.annotation.models.video import Assignment
from global_finprint.annotation.models.observation import MasterRecord


class AssignmentCompareView(UserAllowedMixin, View):
    template_name = 'pages/annotation/assignment_compare.html'

    def get(self, request, set_id):
        set = get_object_or_404(Set, pk=set_id)
        master, created = MasterRecord.objects.get_or_create(set=set)
        context = RequestContext(request, {
            'set': set,
            'video_length': set.video.length(),
            'master': master
        })
        return render_to_response(self.template_name, context=context)


class MasterReviewView(UserAllowedMixin, View):
    template_name = 'pages/annotation/master_review.html'

    def get(self, request, master_id):
        master_record = get_object_or_404(MasterRecord, pk=master_id)
        context = RequestContext(request, {
            'master': master_record,
            'for': ' for {}'.format(master_record.set)
        })
        return render_to_response(self.template_name, context=context)


class AssignmentDetailView(UserAllowedMixin, View):
    def get(self, _, assignment_id):
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        return JsonResponse({
            'observations': list(a.to_json(for_web=True)
                                 for a in sorted(assignment.observation_set.all(),
                                                 key=lambda x: x.initial_observation_time()))
        })


class GetMasterView(UserAllowedMixin, View):
    def get(self, _, set_id):
        master = get_object_or_404(MasterRecord, set=get_object_or_404(Set, pk=set_id))
        return JsonResponse(master.to_json())

    def post(self, request, set_id):
        master_record = get_object_or_404(MasterRecord, set=get_object_or_404(Set, pk=set_id))
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
    def get(self, request, master_id):
        master = get_object_or_404(MasterRecord, pk=master_id)
        master.completed = (request.GET.get('checked', 'false') == 'true')
        master.save()
        return JsonResponse({'success': 'ok'})


class MasterSetDeprecated(UserAllowedMixin, View):
    def get(self, request, master_id):
        master = get_object_or_404(MasterRecord, pk=master_id)
        master.deprecated = (request.GET.get('checked', 'false') == 'true')
        master.save()
        return JsonResponse({'success': 'ok'})

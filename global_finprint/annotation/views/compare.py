from django.views.generic import View
from django.template import RequestContext
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render_to_response
from global_finprint.core.mixins import UserAllowedMixin
from global_finprint.bruv.models import Set
from global_finprint.annotation.models.video import Assignment


class AssignmentCompareView(UserAllowedMixin, View):
    template_name = 'pages/annotation/assignment_compare.html'

    def get(self, request, set_id):
        set = get_object_or_404(Set, pk=set_id)
        context = RequestContext(request, {
            'set': set,
            'video_length': set.video.length()
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

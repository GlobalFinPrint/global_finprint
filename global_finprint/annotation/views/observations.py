from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404

from global_finprint.annotation.models.observation import Observation
from global_finprint.bruv.models import Set, Trip
from global_finprint.core.mixins import UserAllowedMixin


# deprecated:
@login_required
def observation_detail(request, pk):
    observation = Observation.objects.get(pk=pk)
    data = {
            'id': str(observation.id),
            # 'initial_observation_time': observation.initial_observation_time.isoformat(),
            'animal': str(observation.animal),
            'sex': observation.sex,
            'stage': observation.stage,
            'length': str(observation.length),
            'behavior': observation.behavior,
            'set': str(observation.set),
            'observer': str(observation.observer),
            }
    return JsonResponse(data)


def observation_post(request):
    pass


class ObservationListView(UserAllowedMixin, ListView):
    model = Observation
    context_object_name = 'observations'
    template_name = 'pages/observations/observation_list.html'

    def get_queryset(self):
        return get_object_or_404(Set, pk=self.kwargs['set_pk']).observations()

    def get_context_data(self, **kwargs):
        context = super(ObservationListView, self).get_context_data(**kwargs)
        context['trip_pk'] = self.kwargs['trip_pk']
        context['set_pk'] = self.kwargs['set_pk']
        context['trip_name'] = str(Trip.objects.get(pk=self.kwargs['trip_pk']))
        context['set_name'] = str(Set.objects.get(pk=self.kwargs['set_pk']))
        context['for'] = ' for {0}'.format(context['set_name'])
        return context

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib import messages
from django.http.response import JsonResponse
from django.core.urlresolvers import reverse_lazy

from global_finprint.annotation.models import Observation
from global_finprint.bruv.models import Set, Trip
from global_finprint.bruv.forms import ObservationForm


def observation_detail(request, pk):
    observation = Observation.objects.get(pk=pk)
    data = {
            'id': str(observation.id),
            'initial_observation_time': observation.initial_observation_time.isoformat(),
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


class ObservationListView(LoginRequiredMixin, ListView):
    model = Observation
    context_object_name = 'observations'
    template_name = 'pages/observations/observation_list.html'

    def get_queryset(self):
        return Observation.objects.filter(set=self.kwargs['set_pk'])

    def get_context_data(self, **kwargs):
        context = super(ObservationListView, self).get_context_data(**kwargs)
        context['trip_pk'] = self.kwargs['trip_pk']
        context['set_pk'] = self.kwargs['set_pk']
        context['trip_name'] = str(Trip.objects.get(pk=self.kwargs['trip_pk']))
        context['set_name'] = str(Set.objects.get(pk=self.kwargs['set_pk']))
        return context


class ObservationCreateView(LoginRequiredMixin, CreateView):
    success_msg = 'Observation Created!'
    model = Observation
    form_class = ObservationForm
    template_name = 'pages/observations/observation_detail.html'

    context_object_name = 'observation'

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(ObservationCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('set_observation_list', args=[self.kwargs['trip_pk'], self.kwargs['set_pk']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip_pk'] = self.kwargs['trip_pk']
        context['set_pk'] = self.kwargs['set_pk']
        context['trip_name'] = str(Trip.objects.get(pk=self.kwargs['trip_pk']))
        context['set_name'] = str(Set.objects.get(pk=self.kwargs['set_pk']))
        context['obs_name'] = 'Create'
        return context


class ObservationUpdateView(LoginRequiredMixin, UpdateView):
    success_msg = 'Observation Updated'
    model = Observation
    form_class = ObservationForm
    template_name = 'pages/observations/observation_detail.html'

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(ObservationUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('set_observation_list', args=[self.kwargs['trip_pk'], self.kwargs['set_pk']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip_pk'] = self.kwargs['trip_pk']
        context['set_pk'] = self.kwargs['set_pk']
        context['trip_name'] = str(self.object.set.trip)
        context['set_name'] = str(self.object.set)
        context['obs_name'] = str(self.object)
        return context


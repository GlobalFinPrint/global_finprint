from django.views.generic import UpdateView, CreateView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from braces.views import LoginRequiredMixin
from ..models import EnvironmentMeasure, Set, Trip
from ..forms import EnvironmentMeasureForm


class EnvironmentMeasureCreateView(LoginRequiredMixin, CreateView):
    success_msg = 'Environment measure created!'
    model = EnvironmentMeasure
    form_class = EnvironmentMeasureForm
    template_name = 'pages/environmentmeasure/environmentmeasure.html'

    context_object_name = 'environmentmeasure'

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trip_set_list', args=[self.kwargs['trip_pk']])

    def get_context_data(self, **kwargs):
        parent_set = Set.objects.get(id=self.kwargs['trip_pk'])
        initial = {'set': self.kwargs['set_pk'], 'measurement_time': parent_set.drop_time}
        context = super().get_context_data(**kwargs)
        context['trip_pk'] = self.kwargs['trip_pk']
        context['set_pk'] = self.kwargs['set_pk']
        context['form'] = EnvironmentMeasureForm(self.request.POST or None, initial=initial)
        context['trip_name'] = str(Trip.objects.get(pk=self.kwargs['trip_pk']))
        context['set_name'] = str(Set.objects.get(pk=self.kwargs['set_pk']))
        context['env_name'] = 'Create'
        return context


class EnvironmentMeasureUpdateView(LoginRequiredMixin, UpdateView):
    success_msg = 'Environment Measure Created!'
    model = EnvironmentMeasure
    form_class = EnvironmentMeasureForm
    template_name = 'pages/environmentmeasure/environmentmeasure.html'

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trip_set_list', args=[self.kwargs['trip_pk']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip_pk'] = self.kwargs['trip_pk']
        context['set_pk'] = self.kwargs['set_pk']
        context['trip_name'] = str(Trip.objects.get(pk=self.kwargs['trip_pk']))
        context['set_name'] = str(Set.objects.get(pk=self.kwargs['set_pk']))
        context['env_name'] = str(self.object)
        return context

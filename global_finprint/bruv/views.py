from django.views.generic import ListView, UpdateView, CreateView
from django.contrib import messages
from django.http.response import JsonResponse
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin

from global_finprint.bruv.models import Set, Observation
from global_finprint.bruv.forms import SetForm


def set_detail(request, pk):
    s = Set.objects.get(pk=pk)
    data = {'name': str(s),
            'drop_time': s.drop_time.isoformat(),
            'collection_time': s.collection_time.isoformat(),
            'time_bait_gone': s.time_bait_gone.isoformat(),
            'equipment': str(s.equipment),
            'depth': s.depth,
            'reef': str(s.reef)}
    return JsonResponse(data)


class SetListView(ListView):
    model = Set
    context_object_name = 'sets'
    template_name = 'pages/set_list.html'

    def get_queryset(self):
        return Set.objects.filter(trip=self.kwargs['trip_pk'])

    def get_context_data(self, **kwargs):
        context = super(SetListView, self).get_context_data(**kwargs)
        context['trip_pk'] = self.kwargs['trip_pk']
        return context


class SetActionMixin(object):
    form_class = SetForm
    model = Set
    context_object_name = 'set'
    #success_url = reverse_lazy('trip_list')
    #cancel_url = reverse_lazy('trip_list')
    template_name = 'pages/set_detail.html'

    @property
    def success_msg(self):
        return NotImplemented

    def get_success_url(self):
        return reverse_lazy('trip_list', kwargs={'trip_pk': self.kwargs['trip_pk']})

    def get_cancel_url(self):
        return reverse_lazy('trip_list', kwargs={'trip_pk': self.kwargs['trip_pk']})


class SetCreateView(LoginRequiredMixin, SetActionMixin, CreateView):
    success_msg = 'Set Created!'
    context_object_name = 'set'

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(SetActionMixin, self).form_valid(form)


class SetUpdateView(LoginRequiredMixin, SetActionMixin, UpdateView):
    success_msg = 'Set Updated'

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(SetActionMixin, self).form_valid(form)


class ObservationListView(ListView):
    model = Observation
from django.views.generic import UpdateView, CreateView
from django.contrib import messages
from django.http.response import JsonResponse
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin

from global_finprint.trip.models import Trip
from ..models import Set
from ..forms import SetForm


def set_detail(request, pk):
    s = Set.objects.get(pk=pk)
    data = {'id': str(s.id),
            'name': str(s),
            'drop_time': s.drop_time.isoformat(),
            'collection_time': s.collection_time.isoformat() if s.collection_time else None,
            'equipment': str(s.equipment),
            'depth': s.depth,
            'reef': str(s.reef)}
    return JsonResponse(data)


class SetListView(CreateView):
    success_msg = 'Set Created!'
    model = Set
    form_class = SetForm
    context_object_name = 'set'
    template_name = 'pages/sets/set_list.html'

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trip_set_list', args=[self.request.POST['trip']])

    def get_context_data(self, **kwargs):
        parent_trip = Trip.objects.get(id=self.kwargs['trip_pk'])
        form_defaults = {
            'trip': parent_trip,
            'drop_time': parent_trip.start_date,
            'collection_time': parent_trip.start_date,
        }

        context = super(SetListView, self).get_context_data(**kwargs)
        context['sets'] = Set.objects.filter(trip=self.kwargs['trip_pk'])\
            .prefetch_related('environmentmeasure_set')
        context['trip_pk'] = self.kwargs['trip_pk']
        context['trip_name'] = str(Trip.objects.get(pk=self.kwargs['trip_pk']))
        context['set_form'] = SetForm(initial=form_defaults)
        return context


class SetUpdateView(LoginRequiredMixin, UpdateView):
    success_msg = 'Set Updated'
    model = Set
    form_class = SetForm
    template_name = 'pages/sets/set_detail.html'

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(SetUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trip_set_list', args=[self.request.POST['trip']])

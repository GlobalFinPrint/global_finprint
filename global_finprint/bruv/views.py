from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse, DjangoJSONEncoder
from braces.views import LoginRequiredMixin
from global_finprint.bruv.models import Set, Observation
from global_finprint.bruv.forms import SetForm
from django.core.urlresolvers import reverse_lazy


def set_detail(request, pk):
    s = Set.objects.get(pk=pk)
    data = {'name': str(s)}
    return JsonResponse(data)


class SetListView(ListView):
    model = Set
    context_object_name = 'sets'
    template_name = 'pages/set_list.html'

    def get_queryset(self):
        return Set.objects.filter(trip=self.kwargs['trip_pk'])


class SetActionMixin(object):
    form_class = SetForm
    model = Set
    context_object_name = 'set'
    success_url = reverse_lazy('trip_list')
    cancel_url = reverse_lazy('trip_list')
    template_name = 'pages/set_detail.html'

    @property
    def success_msg(self):
        return NotImplemented


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
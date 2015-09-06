from django.views.generic import ListView, DetailView, UpdateView, CreateView, View
from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse, DjangoJSONEncoder
from django.core import serializers
from braces.views import LoginRequiredMixin
from global_finprint.trip.forms import TripForm
from global_finprint.trip.models import Trip
from django.core.urlresolvers import reverse_lazy
import json


class TripActionMixin(object):
    template_name = 'pages/trip_detail.html'

    @property
    def success_msg(self):
        return NotImplemented


class TripListView(ListView):
    model = Trip
    template_name = 'pages/trip_list.html'
    context_object_name = 'trips'

    def get_queryset(self):
        return Trip.objects.all()


class TripDetailView(DetailView):
    form_class = TripForm
    model = Trip
    template_name = 'pages/trip_detail.html'


def trip_detail(request, pk):
    t = Trip.objects.get(pk=pk)
#    data = serializers.serialize('json', t._meta.__dict__)
    data = {'name': str(t),
            'start_date': t.start_date,
            'end_date':t.end_date,
            'location': str(t.location),
            'team': str(t.team),
            'boat': t.boat,
            'type': t.type}
    return JsonResponse(data)


class TripCreateView(LoginRequiredMixin, TripActionMixin, CreateView):
    form_class = TripForm
    model = Trip
    success_msg = 'Trip Created!'
    context_object_name = 'trip'
    success_url = reverse_lazy('trip_list')

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(TripActionMixin, self).form_valid(form)


class TripUpdateView(LoginRequiredMixin, TripActionMixin, UpdateView):
    form_class = TripForm
    model = Trip
    success_msg = 'Trip Updated'
    context_object_name = 'trip'
    success_url = reverse_lazy('trip_list')
    cancel_url = reverse_lazy('trip_list')

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(TripActionMixin, self).form_valid(form)

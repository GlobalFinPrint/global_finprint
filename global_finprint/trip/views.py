from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib import messages
from braces.views import LoginRequiredMixin
from global_finprint.trip.forms import TripForm
from global_finprint.trip.models import Trip
from django.core.urlresolvers import reverse_lazy


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


class TripCreateView(LoginRequiredMixin, TripActionMixin, CreateView):
    form_class = TripForm
    model = Trip
    success_msg = 'Trip Created!'
    context_object_name = 'trip'
    success_url = reverse_lazy('trips')

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(TripActionMixin, self).form_valid(form)


class TripUpdateView(LoginRequiredMixin, TripActionMixin, UpdateView):
    form_class = TripForm
    model = Trip
    success_msg = 'Trip Updated'
    context_object_name = 'trip'
    success_url = reverse_lazy('trips')

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(TripActionMixin, self).form_valid(form)

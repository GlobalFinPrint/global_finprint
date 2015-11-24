from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib import messages
from django.core.serializers import serialize
from django.http.response import JsonResponse, HttpResponse
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin

from .forms import TripForm, TripSearchForm
from .models import Trip
from ..bruv.models import Set


class TripActionMixin(object):
    template_name = 'pages/trips/trip_detail.html'

    @property
    def success_msg(self):
        return NotImplemented


class TripListView(ListView):
    model = Trip
    template_name = 'pages/trips/trip_list.html'
    context_object_name = 'trips'
    trip_form = TripForm
    search_form = TripSearchForm

    def get_queryset(self):
        if self.request.GET:
            search_terms = dict((key, val) for (key, val) in self.request.GET.items()
                                if key in ['location', 'team'] and val != '')
            if 'start_date' in self.request.GET and self.request.GET['start_date'] != '':
                search_terms['start_date__gte'] = self.request.GET['start_date']
            if 'end_date' in self.request.GET and self.request.GET['end_date'] != '':
                search_terms['end_date__lte'] = self.request.GET['end_date']
            return Trip.objects.filter(**search_terms)
        else:
            return Trip.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = TripSearchForm(self.request.GET or None)
        context['trip_form'] = TripForm()
        return context


class TripDetailView(DetailView):
    form_class = TripForm
    model = Trip
    template_name = 'pages/trips/trip_detail.html'


def trip_detail(request, pk):
    t = Trip.objects.get(pk=pk)
    data = {'id': str(t.id),
            'name': str(t),
            'start_date': t.start_date,
            'end_date': t.end_date,
            'location': str(t.location),
            'team': str(t.team),
            'boat': t.boat}
    return JsonResponse(data)


def trip_sets_geojson(request, trip_id):
    feature = serialize('geojson',
                        Set.objects.filter(trip_id=trip_id),
                        fields='coordinates, drop_time'
                        )
    return HttpResponse(feature, content_type='application/json')


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

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib import messages
from django.core.serializers import serialize
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404

from .forms import TripForm, TripSearchForm
from .models import Trip
from ..habitat.models import Region
from ..bruv.models import Set


class TripListView(LoginRequiredMixin, CreateView):
    model = Trip
    form_class = TripForm
    context_object_name = 'trip'
    template_name = 'pages/trips/trip_list.html'
    success_msg = 'Trip created'
    success_url = reverse_lazy('trip_list')

    def form_invalid(self, form):
        messages.error(self.request, 'Form errors found')
        return super().form_invalid(form)

    def form_valid(self, form):
        if 'trip_pk' in self.kwargs:
            edited_trip = get_object_or_404(Trip, pk=self.kwargs['trip_pk'])
            for k, v in form.cleaned_data.items():
                setattr(edited_trip, k, v)
            edited_trip.save()
            messages.success(self.request, 'Trip updated')
            return HttpResponseRedirect(self.success_url)
        else:
            messages.success(self.request, self.success_msg)
            return super().form_valid(form)

    def get_queryset(self):
        form = TripSearchForm(self.request.GET)
        if self.request.GET and form.is_valid():
            search_values = form.cleaned_data
            search_terms = dict((key, val) for (key, val) in search_values.items()
                                if key in ['location', 'team'] and val is not None)

            if search_values['search_start_date']:
                search_terms['start_date__gte'] = search_values['search_start_date']

            if search_values['search_end_date']:
                search_terms['end_date__lte'] = search_values['search_end_date']

            if search_values['region']:
                search_terms['location__in'] = Region.objects.get(pk=search_values['region'].id) \
                    .location_set.values_list('id', flat=True)

            return Trip.objects.filter(**search_terms)
        else:
            return Trip.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trips'] = self.get_queryset()
        context['search_form'] = TripSearchForm(self.request.GET or None)
        if 'trip_pk' in self.kwargs:
            context['trip_pk'] = self.kwargs['trip_pk']
            trip = get_object_or_404(Trip, pk=self.kwargs['trip_pk'])
            context['trip_name'] = str(trip)
            context['trip_form'] = TripForm(instance=trip)
        else:
            context['trip_form'] = TripForm(self.request.POST or None)
        return context


# deprecated:
@login_required
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


@login_required
def trip_sets_geojson(request, trip_id):
    feature = serialize('geojson',
                        Set.objects.filter(trip_id=trip_id),
                        fields='coordinates, drop_time'
                        )
    return HttpResponse(feature, content_type='application/json')

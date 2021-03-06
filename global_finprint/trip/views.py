from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.db.models import F
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers import serialize
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404

from .forms import TripForm, TripSearchForm
from .models import Trip
from ..habitat.models import Region
from ..bruv.models import Set
from ..core.mixins import UserAllowedMixin


class TripListView(UserAllowedMixin, CreateView):
    """
    View for trip list found at /trips/
    """
    model = Trip
    form_class = TripForm
    context_object_name = 'trip'
    template_name = 'pages/trips/trip_list.html'
    success_msg = 'Trip created'
    success_url = reverse_lazy('trip_list')

    def get_form(self, **kwargs):
        """
        Return trip form based on url
        :param kwargs:
        :return:
        """
        if 'trip_pk' in self.kwargs:
            edited_trip = get_object_or_404(Trip, pk=self.kwargs['trip_pk'])
            form = TripForm(self.request.POST or None, instance=edited_trip)
        else:
            form = TripForm(self.request.POST or None)
        return form

    def form_invalid(self, form):
        """
        Invalid form handler method
        :param form:
        :return:
        """
        messages.error(self.request, 'Form errors found')
        return super().form_invalid(form)

    def form_valid(self, form):
        """
        Valid form handler method
        :param form:
        :return:
        """
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
        """
        Get queryset based on search form
        :return:
        """
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

            if search_values['reef']:
                search_terms['set__reef_habitat__reef'] = search_values['reef']

            return Trip.objects.filter(**search_terms).distinct().order_by('start_date').prefetch_related('location__region', 'team__lead__user', 'set_set', 'source')
        else:
            return Trip.objects.all().order_by('start_date').prefetch_related('location__region', 'team__lead__user', 'set_set', 'source')

    def get_context_data(self, **kwargs):
        """
        Get context data for template
        :param kwargs:
        :return:
        """
        page = self.request.GET.get('page', 1)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 50)
        context = super().get_context_data(**kwargs)
        try:
            context['trips'] = paginator.page(page)
        except PageNotAnInteger:
            context['trips'] = paginator.page(1)
        except EmptyPage:
            context['trips'] = paginator.page(paginator.num_pages)
        context['search_form'] = TripSearchForm(self.request.GET or None)
        if 'trip_pk' in self.kwargs:
            context['trip_pk'] = self.kwargs['trip_pk']
            trip = get_object_or_404(Trip, pk=self.kwargs['trip_pk'])
            context['trip_name'] = str(trip)
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


def trip_sets_geojson(request, trip_id):
    """
    Get geoJSON per set for specified trip
    :param request:
    :param trip_id:
    :return:
    """
    set_markers = Set.objects.filter(trip_id=trip_id)
    feature = serialize('geojson',
                        set_markers,
                        fields='coordinates, drop_time, code',
                        )
    return HttpResponse(feature, content_type='application/json')

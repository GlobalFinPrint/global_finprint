from django.views.generic import UpdateView, CreateView
from django.contrib import messages
from django.http.response import JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from braces.views import LoginRequiredMixin

from global_finprint.trip.models import Trip
from global_finprint.bruv.models import Equipment
from ..models import Set
from ..forms import SetForm, EnvironmentMeasureForm

from datetime import datetime
from pytz import timezone


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
    success_msg = 'Set and environmental measure saved!'
    model = Set
    form_class = SetForm
    context_object_name = 'set'
    template_name = 'pages/sets/set_list.html'

    def form_valid(self, form):
        drop_form = EnvironmentMeasureForm(self.request.POST or None, prefix='drop')
        haul_form = EnvironmentMeasureForm(self.request.POST or None, prefix='haul')

        if not drop_form.is_valid():
            return super().form_invalid(drop_form)
        if not haul_form.is_valid():
            return super().form_invalid(haul_form)

        if 'set' in form.cleaned_data:
            edited_set = get_object_or_404(Set, pk=form.cleaned_data['set'])
            for k, v in form.cleaned_data.items():
                setattr(edited_set, k, v)
            for k, v in drop_form.cleaned_data.items():
                setattr(edited_set.drop_measure, k, v)
            for k, v in haul_form.cleaned_data.items():
                setattr(edited_set.haul_measure, k, v)
            edited_set.save()
            edited_set.drop_measure.save()
            edited_set.haul_measure.save()
        else:
            form.cleaned_data['drop_measure'] = drop_form.save()
            form.cleaned_data['haul_measure'] = haul_form.save()
            new_set = Set(**form.cleaned_data)
            new_set.save()

        messages.info(self.request, self.success_msg)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('trip_set_list', args=[self.request.POST['trip']]) + '#'

    def get_context_data(self, **kwargs):
        parent_trip = Trip.objects.get(id=self.kwargs['trip_pk'])
        last_set = parent_trip.set_set.last()
        default_date = timezone('UTC').localize(
            datetime.combine(parent_trip.start_date, datetime.min.time()))

        form_defaults = {
            'trip': parent_trip,
            'drop_time': default_date,
            'collection_time': default_date,
            'equipment': Equipment.objects.all().first()
        }

        if last_set is not None:
            form_defaults.update({
                'reef': last_set.reef,
                'latitude': round(last_set.latitude, 1),
                'longitude': round(last_set.longitude, 1),
                'bait': last_set.bait,
                'bait_oiled': last_set.bait_oiled,
                'visibility': last_set.visibility,
            })

        context = super(SetListView, self).get_context_data(**kwargs)
        context['sets'] = Set.objects.filter(trip=self.kwargs['trip_pk']).order_by('drop_time')
        context['trip_pk'] = self.kwargs['trip_pk']
        context['trip_name'] = str(Trip.objects.get(pk=self.kwargs['trip_pk']))

        if 'set_pk' in self.kwargs:
            edited_set = get_object_or_404(Set, pk=self.kwargs['set_pk'])

            context['set_pk'] = edited_set.id
            context['set_name'] = str(edited_set)

            context['set_form'] = SetForm(
                instance=edited_set,
                trip_pk=self.kwargs['trip_pk'],
                initial={'set': edited_set.id}
            )
            context['drop_form'] = EnvironmentMeasureForm(instance=edited_set.drop_measure, prefix='drop')
            context['haul_form'] = EnvironmentMeasureForm(instance=edited_set.haul_measure, prefix='haul')
        else:
            context['set_form'] = SetForm(
                self.request.POST or None,
                initial=form_defaults,
                trip_pk=self.kwargs['trip_pk']
            )
            context['drop_form'] = EnvironmentMeasureForm(self.request.POST or None, prefix='drop')
            context['haul_form'] = EnvironmentMeasureForm(self.request.POST or None, prefix='haul')
        return context

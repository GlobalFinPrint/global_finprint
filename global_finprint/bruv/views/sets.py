from django.views.generic import UpdateView, CreateView
from django.contrib import messages
from django.http.response import JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from braces.views import LoginRequiredMixin

from global_finprint.trip.models import Trip
from global_finprint.bruv.models import Equipment
from ..models import Set, EnvironmentMeasure
from ..forms import SetForm, EnvironmentMeasureForm


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
    success_msg = 'Set and environmental measure created!'
    model = Set
    form_class = SetForm
    context_object_name = 'set'
    template_name = 'pages/sets/set_list.html'

    def form_valid(self, form):
        env_form = EnvironmentMeasureForm(self.request.POST)
        env_form.fields['set'].required = False
        if env_form.is_valid():
            messages.info(self.request, self.success_msg)
            new_set = Set(**form.cleaned_data)
            new_set.save()
            env_form.cleaned_data['set'] = new_set
            new_env = EnvironmentMeasure(**env_form.cleaned_data)
            new_env.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super().form_invalid(env_form)

    def get_success_url(self):
        return reverse_lazy('trip_set_list', args=[self.request.POST['trip']])

    def get_context_data(self, **kwargs):
        parent_trip = Trip.objects.get(id=self.kwargs['trip_pk'])
        last_set = parent_trip.set_set.last()
        form_defaults = {
            'trip': parent_trip,
            'drop_time': parent_trip.start_date,
            'collection_time': parent_trip.start_date,
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
        context['sets'] = Set.objects.filter(trip=self.kwargs['trip_pk'])\
            .prefetch_related('environmentmeasure_set')
        context['trip_pk'] = self.kwargs['trip_pk']
        context['trip_name'] = str(Trip.objects.get(pk=self.kwargs['trip_pk']))
        context['set_form'] = SetForm(self.request.POST or None, initial=form_defaults, combined=True)
        context['set_form'].helper.form_tag = False
        context['env_form'] = EnvironmentMeasureForm(self.request.POST or None, combined=True)
        context['env_form'].helper.form_tag = False
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trip_pk'] = self.object.trip.id
        return context

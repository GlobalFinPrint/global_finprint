from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib import messages
from django.http.response import JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from global_finprint.trip.models import Trip
from global_finprint.bruv.models import Equipment
from ..models import Set
from ..forms import SetForm, EnvironmentMeasureForm, BaitForm
from ...annotation.forms import VideoForm
from ...habitat.models import ReefHabitat

from datetime import datetime


# deprecated:
@login_required
def set_detail(request, pk):
    s = Set.objects.get(pk=pk)
    data = {'id': str(s.id),
            'name': str(s),
            'drop_time': s.drop_time.isoformat(),
            'haul_time': s.haul_time.isoformat() if s.haul_time else None,
            'equipment': str(s.equipment),
            'depth': s.depth,
            'reef_habitat': str(s.reef_habitat)}
    return JsonResponse(data)


class SetListView(LoginRequiredMixin, View):
    template = 'pages/sets/set_list.html'

    def _common_context(self, request, parent_trip):
        return RequestContext(request, {
            'request': request,
            'trip_pk': parent_trip.pk,
            'trip_name': str(parent_trip),
            'sets': Set.objects.filter(trip=parent_trip).order_by('drop_time'),
        })

    def _get_set_form_defaults(self, parent_trip):
        set_form_defaults = {
            'trip': parent_trip,
            'set_date': parent_trip.start_date,
            'drop_time': datetime.min.time(),
            'haul_time': datetime.min.time(),
            'equipment': Equipment.objects.all().first(),
        }

        last_set = parent_trip.set_set.last()

        if last_set is not None:
            set_form_defaults.update({
                'reef_habitat': last_set.reef_habitat,
                'latitude': round(last_set.latitude, 1),
                'longitude': round(last_set.longitude, 1),
                'set_date': last_set.set_date,
                'drop_time': last_set.drop_time,
                'haul_time': last_set.haul_time,
                'visibility': last_set.visibility,
            })

        return set_form_defaults

    def get(self, request, **kwargs):
        trip_pk, set_pk = kwargs.get('trip_pk', None), kwargs.get('set_pk', None)
        parent_trip = get_object_or_404(Trip, pk=trip_pk)
        context = self._common_context(request, parent_trip)

        # edit set form
        if set_pk:
            edited_set = get_object_or_404(Set, pk=set_pk)
            context['set_pk'] = set_pk
            context['set_name'] = str(edited_set)
            context['set_form'] = SetForm(
                instance=edited_set,
                trip_pk=trip_pk
            )
            context['set_form'].initial['reef'] = edited_set.reef_habitat.reef
            context['set_form'].initial['habitat'] = edited_set.reef_habitat.habitat
            context['bait_form'] = BaitForm(
                instance=edited_set.bait
            )
            context['drop_form'] = EnvironmentMeasureForm(
                instance=edited_set.drop_measure, prefix='drop'
            )
            context['haul_form'] = EnvironmentMeasureForm(
                instance=edited_set.haul_measure, prefix='haul'
            )
            context['video_form'] = VideoForm(
                instance=edited_set.video
            )

        # new set form
        else:
            context['set_form'] = SetForm(
                None,
                initial=self._get_set_form_defaults(parent_trip),
                trip_pk=trip_pk
            )
            context['bait_form'] = BaitForm(initial={'type': 'CHP'})
            context['drop_form'] = EnvironmentMeasureForm(None, prefix='drop')
            context['haul_form'] = EnvironmentMeasureForm(None, prefix='haul')
            context['video_form'] = VideoForm()

        return render_to_response(self.template, context=context)

    def post(self, request, **kwargs):
        trip_pk, set_pk = kwargs.get('trip_pk', None), kwargs.get('set_pk', None)
        parent_trip = get_object_or_404(Trip, pk=kwargs['trip_pk'])
        context = self._common_context(request, parent_trip)

        set_form = SetForm(request.POST, trip_pk=trip_pk)
        bait_form = BaitForm(request.POST)
        drop_form = EnvironmentMeasureForm(request.POST, prefix='drop')
        haul_form = EnvironmentMeasureForm(request.POST, prefix='haul')
        video_form = VideoForm(request.POST, request.FILES)

        # forms are valid
        if all(form.is_valid() for form in [set_form, bait_form, drop_form, haul_form, video_form]):

            # get reef_habitat from reef + habitat
            # note: "create new set" uses the .instance, "edit existing set" is using the .cleaned_data
            # perhaps do something cleaner?
            set_form.instance.reef_habitat = set_form.cleaned_data['reef_habitat'] = ReefHabitat.get_or_create(
                    reef=set_form.cleaned_data['reef'],
                    habitat=set_form.cleaned_data['habitat'])

            # create new set and env measures
            if set_pk is None:
                new_set = set_form.save()
                new_set.bait = bait_form.save()
                new_set.drop_measure = drop_form.save()
                new_set.haul_measure = haul_form.save()
                new_set.video = video_form.save()
                new_set.save()

                messages.success(self.request, 'Set and drop/haul measures created')

            # edit existing set and env measures
            else:
                edited_set = get_object_or_404(Set, pk=set_pk)
                for k, v in set_form.cleaned_data.items():
                    if k not in ('reef', 'habitat'):
                        setattr(edited_set, k, v)
                for k, v in bait_form.cleaned_data.items():
                    setattr(edited_set.bait, k, v)
                for k, v in drop_form.cleaned_data.items():
                    setattr(edited_set.drop_measure, k, v)
                for k, v in haul_form.cleaned_data.items():
                    setattr(edited_set.haul_measure, k, v)
                for k, v in video_form.cleaned_data.items():
                    setattr(edited_set.video, k, v)

                edited_set.save()
                edited_set.bait.save()
                edited_set.drop_measure.save()
                edited_set.haul_measure.save()
                edited_set.video.save()

                messages.success(self.request, 'Set and drop/haul measures updated')

            # navigate back to set list
            success_url = reverse_lazy('trip_set_list', args=trip_pk)
            return HttpResponseRedirect(success_url)

        # one or more forms have errors
        else:
            context['form_errors'] = True
            if set_pk:
                context['set_pk'] = set_pk
                context['set_name'] = str(get_object_or_404(Set, pk=set_pk))
            context['set_form'] = set_form
            context['bait_form'] = bait_form
            context['drop_form'] = drop_form
            context['haul_form'] = haul_form
            context['video_form'] = video_form

            messages.error(self.request, 'Form errors found')

            return render_to_response(self.template, context=context)

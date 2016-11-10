from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib import messages
from django.http.response import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.db import transaction

from global_finprint.trip.models import Trip
from global_finprint.bruv.models import Equipment
from global_finprint.annotation.models.video import Video
from ..models import Set, HabitatSubstrate, EnvironmentMeasure
from ..forms import SetForm, EnvironmentMeasureForm, \
    SetSearchForm, SetLevelCommentsForm, SetLevelDataForm
from ...annotation.forms import VideoForm
from ...habitat.models import ReefHabitat
from ...core.mixins import UserAllowedMixin

from boto import exception as BotoException
from boto.s3.connection import S3Connection
from django.conf import settings


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


class SetListView(UserAllowedMixin, View):
    template = 'pages/sets/set_list.html'

    def _common_context(self, request, parent_trip):
        page = request.GET.get('page', 1)
        paginator = Paginator(self._get_filtered_sets(parent_trip), 50)
        try:
            sets = paginator.page(page)
        except PageNotAnInteger:
            sets = paginator.page(1)
        except EmptyPage:
            sets = paginator.page(paginator.num_pages)
        return RequestContext(request, {
            'request': request,
            'trip_pk': parent_trip.pk,
            'trip_name': str(parent_trip),
            'sets': sets,
            'search_form': SetSearchForm(self.request.GET or None, trip_id=parent_trip.pk)
        })

    def _get_filtered_sets(self, parent_trip):
        result = Set.objects
        prefetch = [
            'trip',
            'drop_measure',
            'haul_measure',
            'video',
            'user',
            'bait',
            'equipment',
            'reef_habitat',
        ]
        search_terms = {}
        form = SetSearchForm(self.request.GET)
        if self.request.GET and form.is_valid():
            search_values = form.cleaned_data
            search_terms = dict((key, val) for (key, val) in search_values.items()
                                if key in ['equipment', 'bait'] and val is not None)
            if search_values['search_set_date']:
                search_terms['set_date'] = search_values['search_set_date']
            if search_values['reef']:
                search_terms['reef_habitat__reef'] = search_values['reef']
            if search_values['habitat']:
                search_terms['reef_habitat__habitat'] = search_values['habitat']
            if search_values['code']:
                result = result.filter(code__contains=search_values['code'])
        search_terms['trip'] = parent_trip
        result = result.filter(**search_terms).prefetch_related(*prefetch).order_by('set_date', 'drop_time')

        return result

    def _get_set_form_defaults(self, parent_trip):
        set_form_defaults = {
            'trip': parent_trip,
            'set_date': parent_trip.start_date,
            'equipment': Equipment.objects.all().first(),
        }

        last_set = parent_trip.set_set.last()

        if last_set is not None:
            set_form_defaults.update({
                'reef_habitat': last_set.reef_habitat,
                'reef': last_set.reef_habitat.reef,
                'habitat': last_set.reef_habitat.habitat,
                'latitude': last_set.latitude,
                'longitude': last_set.longitude,
                'set_date': last_set.set_date,
                'drop_time': last_set.drop_time,
                'haul_date': last_set.haul_date,
                'haul_time': last_set.haul_time,
                'equipment': last_set.equipment,
                'bait': last_set.bait
            })

        return set_form_defaults

    def _upload_image(self, file, filename):
        try:
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            bucket = conn.get_bucket(settings.HABITAT_IMAGE_BUCKET, validate=False)
            key = bucket.get_key(filename)
            if not key:
                key = bucket.new_key(filename)
            key.set_contents_from_string(file.read(), headers={'Content-Type': 'image/png'})
            key.set_acl('public-read')
            return True, None
        except BotoException.S3ResponseError as e:
            return False, e

    def _process_habitat_images(self, set, request):
        if request.FILES.get('bruv_image_file', False):
            filename = set.habitat_filename('bruv')
            success, error = self._upload_image(request.FILES['bruv_image_file'], filename)
            if success:
                set.bruv_image_url = filename
                set.save()
            else:
                messages.warning(request, 'Error uploading BRUV image: {}'.format(str(error)))

        if request.FILES.get('splendor_image_file', False):
            filename = set.habitat_filename('splendor')
            success, error = self._upload_image(request.FILES['splendor_image_file'], filename)
            if success:
                set.splendor_image_url = filename
                set.save()
            else:
                messages.warning(request, 'Error uploading Habitat image: {}'.format(str(error)))

    def _process_habitat_substrate(self, set, request):
        with transaction.atomic():
            set.substrate.clear()
            for (s_id, val) in zip(request.POST.getlist('substrate'), request.POST.getlist('percent')):
                hs = HabitatSubstrate(set=set, substrate_id=s_id, value=val)
                hs.save()

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

            context['drop_form'] = EnvironmentMeasureForm(
                instance=edited_set.drop_measure, prefix='drop'
            )
            context['haul_form'] = EnvironmentMeasureForm(
                instance=edited_set.haul_measure, prefix='haul'
            )
            context['video_form'] = VideoForm(
                instance=edited_set.video
            )
            context['set_level_data_form'] = SetLevelDataForm(
                instance=edited_set
            )
            context['set_level_comments_form'] = SetLevelCommentsForm(
                instance=edited_set
            )

        # new set form
        else:
            context['set_form'] = SetForm(
                None,
                initial=self._get_set_form_defaults(parent_trip),
                trip_pk=trip_pk
            )
            context['drop_form'] = EnvironmentMeasureForm(None, prefix='drop')
            context['haul_form'] = EnvironmentMeasureForm(None, prefix='haul')
            context['video_form'] = VideoForm()
            context['set_level_data_form'] = SetLevelDataForm()
            context['set_level_comments_form'] = SetLevelCommentsForm()

        return render_to_response(self.template, context=context)

    def post(self, request, **kwargs):
        trip_pk, set_pk = kwargs.get('trip_pk', None), kwargs.get('set_pk', None)
        parent_trip = get_object_or_404(Trip, pk=kwargs['trip_pk'])
        context = self._common_context(request, parent_trip)

        if set_pk is None:
            set_form = SetForm(request.POST, trip_pk=trip_pk)
            drop_form = EnvironmentMeasureForm(request.POST, prefix='drop')
            haul_form = EnvironmentMeasureForm(request.POST, prefix='haul')
            video_form = VideoForm(request.POST)
            set_level_data_form = SetLevelDataForm(request.POST, request.FILES)
            set_level_comments_form = SetLevelCommentsForm(request.POST)
        else:
            edited_set = get_object_or_404(Set, pk=set_pk)
            set_form = SetForm(request.POST, trip_pk=trip_pk, instance=edited_set)
            drop_form = EnvironmentMeasureForm(request.POST, prefix='drop', instance=edited_set.drop_measure)
            haul_form = EnvironmentMeasureForm(request.POST, prefix='haul', instance=edited_set.haul_measure)
            video_form = VideoForm(request.POST, instance=edited_set.video)
            set_level_data_form = SetLevelDataForm(request.POST, request.FILES, instance=edited_set)
            set_level_comments_form = SetLevelCommentsForm(request.POST, instance=edited_set)

        # forms are valid
        if all(form.is_valid() for form in [set_form,
                                            drop_form,
                                            haul_form,
                                            video_form,
                                            set_level_data_form,
                                            set_level_comments_form]):

            # get reef_habitat from reef + habitat
            # note: "create new set" uses the .instance, "edit existing set" is using the .cleaned_data
            # perhaps do something cleaner?
            set_form.instance.reef_habitat = set_form.cleaned_data['reef_habitat'] = ReefHabitat.get_or_create(
                    reef=set_form.cleaned_data['reef'],
                    habitat=set_form.cleaned_data['habitat'])

            # create new set and env measures
            if set_pk is None:
                new_set = set_form.save()
                new_set.drop_measure = drop_form.save()
                new_set.haul_measure = haul_form.save()
                new_set.video = video_form.save()
                for k, v in set_level_data_form.cleaned_data.items():
                    if k not in ('bruv_image_file', 'splendor_image_file'):
                        setattr(new_set, k, v)
                for k, v in set_level_comments_form.cleaned_data.items():
                    setattr(new_set, k, v)
                new_set.save()

                # upload and save image urls
                self._process_habitat_images(new_set, request)

                # save habitat substrate values
                self._process_habitat_substrate(new_set, request)

                messages.success(self.request, 'Set created')

            # edit existing set and env measures
            else:
                for k, v in set_form.cleaned_data.items():
                    if k not in ('reef', 'habitat'):
                        setattr(edited_set, k, v)

                # check for children that might be missing but have data in their forms:
                if not edited_set.drop_measure and \
                    any(x is not None for x in list(drop_form.cleaned_data.values())):
                    # note: the dissolved_oxygen_measure shows up as a value and should probably be filtered out ...
                    # otherwise measure is always created.
                    edited_set.drop_measure = EnvironmentMeasure.objects.create()
                if not edited_set.haul_measure and \
                    any(x is not None for x in list(haul_form.cleaned_data.values())):
                    # note: again, the dissolved_oxygen_measure shows up as a value and should probably be filtered out?
                    edited_set.haul_measure = EnvironmentMeasure.objects.create()

                # guard against possibly missing drop_measure, haul_measure or video:
                if edited_set.drop_measure:
                    for k, v in drop_form.cleaned_data.items():
                        setattr(edited_set.drop_measure, k, v)
                if edited_set.haul_measure:
                    for k, v in haul_form.cleaned_data.items():
                        setattr(edited_set.haul_measure, k, v)
                for k, v in video_form.cleaned_data.items():
                    setattr(edited_set.video, k, v)
                for k, v in set_level_data_form.cleaned_data.items():
                    if k not in ('bruv_image_file', 'splendor_image_file'):
                        setattr(edited_set, k, v)
                for k, v in set_level_comments_form.cleaned_data.items():
                    setattr(edited_set, k, v)

                edited_set.save()
                if edited_set.bait:
                    edited_set.bait.save()
                if edited_set.drop_measure:
                    edited_set.drop_measure.save()
                if edited_set.haul_measure:
                    edited_set.haul_measure.save()
                edited_set.video.save()

                # upload and save image urls
                self._process_habitat_images(edited_set, request)

                # save habitat substrate values
                self._process_habitat_substrate(edited_set, request)

                messages.success(self.request, 'Set updated')

            # navigate back to set list
            success_url = reverse_lazy('trip_set_list', args=[trip_pk])
            if 'save-and-add' in request.POST:
                success_url += '#set-form-parent'
            else:
                success_url += '#'
            return HttpResponseRedirect(success_url)

        # one or more forms have errors
        else:
            context['form_errors'] = True
            if set_pk:
                context['set_pk'] = set_pk
                context['set_name'] = str(get_object_or_404(Set, pk=set_pk))
            context['set_form'] = set_form
            context['drop_form'] = drop_form
            context['haul_form'] = haul_form
            context['video_form'] = video_form
            context['set_level_data_form'] = set_level_data_form
            context['set_level_comments_form'] = set_level_comments_form

            messages.error(self.request, 'Form errors found')

            return render_to_response(self.template, context=context)

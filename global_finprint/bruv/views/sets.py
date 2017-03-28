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
from ..models import Set, BenthicCategoryValue, EnvironmentMeasure, Bait, Video
from ..forms import SetForm, EnvironmentMeasureForm, \
    SetSearchForm, SetLevelCommentsForm, SetLevelDataForm, SetBulkUploadForm
from ...annotation.forms import VideoForm
from ...annotation.models.video import VideoFile
from ...habitat.models import ReefHabitat, Reef, ReefType
from ...core.mixins import UserAllowedMixin

from boto import exception as BotoException
from boto.s3.connection import S3Connection
from django.conf import settings
from openpyxl import load_workbook
from io import BytesIO
from zipfile import BadZipFile
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


class BulkImportError(Exception):
    pass


class SetBulkUploadView(UserAllowedMixin, View):
    template = 'pages/sets/bulk_upload.html'

    def get(self, request, **kwargs):
        return HttpResponseRedirect(reverse_lazy('trip_set_list', args=[kwargs.get('trip_pk', None)]))

    def post(self, request, **kwargs):
        trip_id = kwargs.get('trip_pk', None)
        error_message = ''
        form = SetBulkUploadForm(request.POST, request.FILES, trip_id=trip_id)
        if not form.is_valid():
            invalid_url = reverse_lazy('trip_set_list', args=[trip_id])
            messages.error(request, 'Invalid bulk upload form')
            return HttpResponseRedirect(invalid_url)
        file = request.FILES['set_file']
        sheet_context = ''
        try:
            workbook = load_workbook(BytesIO(file.read()), read_only=True)
            set_sheet = workbook.get_sheet_by_name('Set')
            env_sheet = workbook.get_sheet_by_name('Environment')
            if not list(set_sheet.rows)[1:]:
                raise BulkImportError('Bulk upload spreadsheet is empty.')

            with transaction.atomic():
                trip_dict = dict(Trip.objects.values_list('code', 'id'))
                bait_dict = dict((str(b), b.id) for b in Bait.objects.all())
                equipment_dict = dict((str(e), e.id) for e in Equipment.objects.all())
                reef_dict = dict((u'{}|{}'.format(r.site.name, r.name), r.id) for r in Reef.objects.all())
                habitat_dict = dict((str(h), h.id) for h in ReefType.objects.all())
                set_fields = [
                    'trip_code', 'set_code', 'date',
                    'latitude', 'longitude', 'depth',
                    'drop_time', 'haul_time', 'site',
                    'reef', 'habitat', 'equipment',
                    'bait', 'visibility',
                    'current_flow_estimated', 'current_flow_instrumented',
                    'video_file_name', 'video_source', 'video_path',
                    'comment'
                ]
                set_fields_dict = dict((cell.value, n) for n, cell in enumerate(list(set_sheet.rows)[0])
                                       if cell.value in set_fields)
                env_fields = [
                    'trip_code', 'set_code',
                    'drop_haul', 'temp', 'salinity',
                    'conductivity', 'dissolved_oxygen',
                    'current_direction', 'tide_state',
                    'estimated_wind_speed', 'measured_wind_speed',
                    'wind_direction', 'cloud_cover', 'surface_chop'
                ]
                env_fields_dict = dict((cell.value, n) for n, cell in enumerate(list(env_sheet.rows)[0])
                                       if cell.value in env_fields)

                sheet_context = 'set'
                for i, row in enumerate(list(set_sheet.rows)[1:]):
                    if row[0].value is None:
                        if i == 0:
                            # there are default values in row 2 or there's some data further
                            # down in the sheet but row 2 is mysteriously empty ...
                            raise BulkImportError('Bulk upload spreadsheet is empty.')
                        else:
                            break
                    new_video = Video()
                    new_video.save()
                    if row[set_fields_dict['video_file_name']].value is not None:
                        new_video_file = VideoFile(
                            file=row[set_fields_dict['video_file_name']].value.strip(),
                            source=(
                                row[set_fields_dict[
                                    'video_source']].value.strip() if 'video_source' in set_fields_dict else 'S3'),
                            path=(
                                row[set_fields_dict[
                                    'video_path']].value.strip() if 'video_path' in set_fields_dict else ''),
                            video=new_video,
                            primary=True)
                        new_video_file.save()

                    new_drop = EnvironmentMeasure()
                    new_drop.save()
                    new_haul = EnvironmentMeasure()
                    new_haul.save()

                    new_set = Set(
                        trip_id=trip_dict[row[set_fields_dict['trip_code']].value.strip()],
                        code=row[set_fields_dict['set_code']].value.strip(),
                        set_date=datetime.strptime(row[set_fields_dict['date']].value, '%d/%m/%Y'),
                        latitude=row[set_fields_dict['latitude']].value,
                        longitude=row[set_fields_dict['longitude']].value,
                        depth=row[set_fields_dict['depth']].value,
                        drop_time=row[set_fields_dict['drop_time']].value,
                        haul_time=row[set_fields_dict['haul_time']].value,
                        reef_habitat=ReefHabitat.get_or_create_by_id(
                            reef_dict[u'{}|{}'.format(row[set_fields_dict['site']].value.strip(),
                                                      row[set_fields_dict['reef']].value.strip())],
                            habitat_dict[row[set_fields_dict['habitat']].value.strip()]
                        ),
                        equipment_id=equipment_dict[row[set_fields_dict['equipment']].value.strip()],
                        bait_id=bait_dict[row[set_fields_dict['bait']].value.strip()],
                        visibility=('' if row[set_fields_dict['visibility']].value is None
                                    else row[set_fields_dict['visibility']].value),
                        current_flow_estimated=('' if row[set_fields_dict['current_flow_estimated']].value is None
                                                else row[set_fields_dict['current_flow_estimated']].value.strip().upper()),
                        current_flow_instrumented=row[set_fields_dict['current_flow_instrumented']].value,
                        comments=('BULK UPLOAD' if row[set_fields_dict['comment']].value.strip() is None
                                  else row[set_fields_dict['comment']].value.strip() + ' -- BULK UPLOAD'),
                        video=new_video,
                        drop_measure=new_drop,
                        haul_measure=new_haul
                    )
                    new_set.save()

                sheet_context = 'environment measure'
                for i, row in enumerate(list(env_sheet.rows)[1:]):
                    if row[0].value is None:
                        break

                    set = Set.objects.get(trip__code=row[env_fields_dict['trip_code']].value.strip(),
                                          code=row[env_fields_dict['set_code']].value.strip())
                    if row[env_fields_dict['drop_haul']].value.strip().lower() == 'drop':
                        env = set.drop_measure
                    elif row[env_fields_dict['drop_haul']].value.strip().lower() == 'haul':
                        env = set.haul_measure
                    else:
                        raise BulkImportError('drop_haul needs to be "drop" or "haul"')

                    env.water_temperature = row[env_fields_dict['temp']].value
                    env.salinity = row[env_fields_dict['salinity']].value
                    env.conductivity = row[env_fields_dict['conductivity']].value
                    env.dissolved_oxygen = row[env_fields_dict['dissolved_oxygen']].value
                    env.tide_state = ('' if row[env_fields_dict['tide_state']].value is None
                                      else row[env_fields_dict['tide_state']].value.strip().upper())  # TODO choice field
                    env.estimated_wind_speed = row[env_fields_dict['estimated_wind_speed']].value
                    env.measured_wind_speed = row[env_fields_dict['measured_wind_speed']].value
                    env.wind_direction = ('' if row[env_fields_dict['wind_direction']].value is None
                                          else row[
                        env_fields_dict['wind_direction']].value.strip().upper())  # TODO choice field
                    env.cloud_cover = row[env_fields_dict['cloud_cover']].value
                    env.surface_chop = ('' if row[env_fields_dict['surface_chop']].value is None
                                        else row[env_fields_dict['surface_chop']].value.strip().upper())  # TODO choice field
                    env.save()

        except BadZipFile:  # xlsx is a zip file (for reals)
            error_message = 'Unexpected file format'
        except Exception as e:
            error_type = e.__class__.__name__
            error_text = str(' '.join(e) if hasattr(e, '__iter__') else str(e))

            if error_type == 'KeyError':
                # todo: KeyError is also raised when the worksheet does not exist.  Can we call that our specifically?
                error_type = 'Value not found in lookup table'
            elif error_type == 'ValidationError' or error_type == 'ValueError':
                error_type = 'Invalid data formatting'
                error_text = error_text.replace('%d/%m/%Y', 'DD/MM/YYYY')
            elif error_type == 'DataError':
                error_type = 'Invalid data value'

            try:
                row = i + 2
            except NameError:
                error_message = '{}: {}'.format(error_type, error_text)
            else:
                error_message = '{} (row {} of {} sheet): {}'.format(error_type, row, sheet_context, error_text)

        success_message = '' if error_message else 'Bulk upload successful!'

        return render_to_response(self.template,
                                  context=RequestContext(request, {'trip_pk': trip_id,
                                                                   'file_name': file.name,
                                                                   'error_message': error_message,
                                                                   'success_message': success_message}))


class SetListView(UserAllowedMixin, View):
    """
    Set list view found at /trips/<trip_id>/sets/
    """
    template = 'pages/sets/set_list.html'

    def _common_context(self, request, parent_trip):
        """
        Helper method returns page context common to multiple requests
        :param request:
        :param parent_trip:
        :return:
        """
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
            'search_form': SetSearchForm(self.request.GET or None, trip_id=parent_trip.pk),
            'bulk_form': SetBulkUploadForm(trip_id=parent_trip.pk)
        })

    def _get_filtered_sets(self, parent_trip):
        """
        Helper method returns sets that match filter
        :param parent_trip:
        :return:
        """
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
        """
        Helper method returns
        :param parent_trip:
        :return:
        """
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
        """
        Helper method uploads image to S3
        :param file:
        :param filename:
        :return:
        """
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
        """
        Helper method processes habitat images
        :param set:
        :param request:
        :return:
        """
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
        """
        Helper method saves habitat substrate data
        :param set:
        :param request:
        :return:
        """
        with transaction.atomic():
            set.benthic_category.clear()
            for (s_id, val) in zip(request.POST.getlist('benthic-category'), request.POST.getlist('percent')):
                bcv = BenthicCategoryValue(set=set, benthic_category_id=s_id, value=val)
                bcv.save()

    def get(self, request, **kwargs):
        """
        Main method to return template
        :param request:
        :param kwargs:
        :return:
        """
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
        """
        Main method to process form submissions
        :param request:
        :param kwargs:
        :return:
        """
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
                for k, v in set_level_data_form.cleaned_data.items():
                    if k not in ('bruv_image_file', 'splendor_image_file', 'benthic_category'):
                        setattr(new_set, k, v)
                for k, v in set_level_comments_form.cleaned_data.items():
                    setattr(new_set, k, v)
                new_set.save()

                # update video
                video_form.save(new_set)

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

                # guard against possibly missing drop_measure, haul_measure:
                if edited_set.drop_measure:
                    for k, v in drop_form.cleaned_data.items():
                        setattr(edited_set.drop_measure, k, v)
                if edited_set.haul_measure:
                    for k, v in haul_form.cleaned_data.items():
                        setattr(edited_set.haul_measure, k, v)
                for k, v in set_level_data_form.cleaned_data.items():
                    if k not in ('bruv_image_file', 'splendor_image_file', 'benthic_category'):
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

                # update video
                video_form.update(edited_set)

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

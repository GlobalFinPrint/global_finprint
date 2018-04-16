from datetime import datetime as dt
from datetime import time
from builtins import set as set_utils

import django.core.exceptions as django_exceptions
from django.views.generic.base import View
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from global_finprint.trip.models import Trip
from global_finprint.annotation.models.animal import Animal
from global_finprint.annotation.models.video import VideoFile, Assignment
from global_finprint.annotation.models.observation import Observation, Attribute, Event, Measurable, EventMeasurable
from global_finprint.core.models import FinprintUser
from global_finprint.core.models import Affiliation
from global_finprint.bruv.models import Set
from global_finprint.habitat.models import Site

MAXN_MEASURABLE_ID = 2

IMAGE_URL_FORMAT = 'https://s3-us-west-2.amazonaws.com/finprint-annotator-screen-captures/prod/{trip_code}/{set_code}/{obs_id}_{event_id}.png'


class APIView(View):
    """
    Main view to be inherited by other views requiring auth (also grabs assignment and user)
    """
    def dispatch(self, request, *args, **kwargs):
        if 'token' in request.GET:
            token = request.GET.get('token', None)
        elif 'token' in request.POST:
            token = request.POST.get('token', None)
        else:
            return HttpResponseForbidden()

        try:
            request.annotator = FinprintUser.objects.get(token=token)
        except FinprintUser.DoesNotExist:
            return HttpResponseForbidden()

        # todo:  2017-12-7 - this does indeed break the annotator client which passes
        # what it calls set_id but what is really assignment_id
        if 'set_id' in kwargs:
            try:
                # In this context set_id is actually the id of an assignment.
                filter_params = { 'pk': kwargs['set_id'] }
                if not request.annotator.is_lead():
                    # only annotators can fetch other user's assignments
                    filter_params['annotator'] = request.annotator
                request.va = Assignment.objects.get(**filter_params)
            except Assignment.DoesNotExist:
                return HttpResponseNotFound()

        return super().dispatch(request, *args, **kwargs)


class Login(View):
    """
    Login view
    """
    def post(self, request):
        user = authenticate(
            username=request.POST.get('username', None),
            password=request.POST.get('password', None))

        if user is None:
            return HttpResponseForbidden()

        try:
            annotator = user.finprintuser
            token = annotator.set_token()
        except FinprintUser.DoesNotExist:
            return HttpResponseForbidden()

        response_json = {
            'user_id': annotator.id,
            'token': token,
            'role': 'lead' if annotator.is_lead() else 'annotator',
        }

        if not request.POST.get('skip_set_list', False):
            assignments = Assignment.get_active().filter(assigned_by=annotator) if annotator.is_lead() \
                else Assignment.get_active_for_annotator(annotator)
            response_json['sets'] = list(va.to_json() for va in assignments)

        return JsonResponse(response_json)


class Logout(APIView):
    """
    Logout view
    """
    def post(self, request):
        request.annotator.clear_token()
        return JsonResponse({'status': 'OK'})


class SetList(APIView):
    """
    Set list view
    """
    def get(self, request):
        if request.annotator.is_lead() and 'filtered' in request.GET:
            if 'assigned_by_me' in request.GET:
                assignments = Assignment.get_active().filter(assigned_by=request.annotator)
            else:
                assignments = Assignment.get_active()
            if 'affiliation_id' in request.GET:
                affiliated_users_set = FinprintUser.objects.all().filter(
                    affiliation_id=request.GET.get('affiliation_id'))
                assignments = assignments.filter(annotator_id__in=affiliated_users_set)
            if 'trip_id' in request.GET:
                assignments = assignments.filter(video__set__trip__id=request.GET.get('trip_id'))
            if 'reef_id' in request.GET:
                assignments = assignments.filter(video__set__reef_habitat__reef_id=request.GET.get('reef_id'))
            if 'set_id' in request.GET:
                assignments = assignments.filter(video__set__id=request.GET.get('set_id'))
            if 'annotator_id' in request.GET:
                assignments = assignments.filter(annotator_id=request.GET.get('annotator_id'))
            if 'status_id' in request.GET:
                assignments = assignments.filter(status_id=request.GET.get('status_id'))
        else:
            assignments = Assignment.get_active_for_annotator(request.annotator)

        return JsonResponse({'sets': list(va.to_json() for va in assignments)})


class TripList(APIView):
    """
    Trip list view (filter on assigned to current user or not)
    """
    def get(self, request):
        if request.GET.get('assigned', False):
            assignments = Assignment.get_active()
            sets = set(a.set() for a in assignments)
            trips = sorted(set(s.trip for s in sets), key=str)
            return JsonResponse({'trips': list({'id': t.id, 'trip': str(t),
                                                'sets': list({'id': s.id, 'set': s.code}
                                                             for s in t.set_set.all().order_by('code')
                                                             if s in sets)}
                                               for t in trips)})
        else:
            trips = sorted(Trip.objects.all(), key=str)
            return JsonResponse({'trips': list({'id': t.id, 'trip': str(t),
                                                'sets': list({'id': s.id, 'set': s.code}
                                                             for s in t.set_set.all().order_by('code'))}
                                               for t in trips)})


class AnnotatorList(APIView):
    """
    Annotator list view
    """
    def get(self, request):
        assignments = Assignment.get_active()
        return JsonResponse({'annotators': list({'id': an.id, 'annotator': str(an)}
                                                for an in sorted(set(a.annotator for a in assignments), key=str))})


class SetDetail(APIView):
    """
    Set detail view
    """
    def get(self, request, set_id):
        return JsonResponse({'set': {'id': request.va.id,
                                     'set_code': str(request.va.set()),
                                     'file': str(request.va.video.primary()),
                                     'assigned_to': {'id': request.va.annotator_id,
                                                     'user': str(request.va.annotator)},
                                     'progress': request.va.progress,
                                     'observations': Observation.get_for_api(request.va),
                                     'animals': Animal.get_for_api(request.va),
                                     'status': {'id': request.va.status_id,
                                                'name': request.va.status.name}
                                     }})


class VideoDetail(APIView):
    """
    Video detail view
    """
    def get(self, request, file_name):
        video_list = []
        video_files = VideoFile.objects.filter(file=file_name)
        for video_file in video_files:
            try:
                assignment = video_file.video.assignment_set.get(annotator=request.annotator)
            except django_exceptions.ObjectDoesNotExist:
                assignment = None
            video_list.append(
                {
                    'file': video_file.file,
                    'source': video_file.source,
                    'path': video_file.path,
                    'rank': video_file.rank,
                    'primary': video_file.primary,
                    'video': {
                        'id': video_file.video.id,
                        'set_id': assignment.id if assignment else None,
                        'set_code': video_file.video.set.code,
                        'trip_code': video_file.video.set.trip.code
                    }
                }
            )
        return JsonResponse({'videos': video_list})


class Observations(APIView):
    """
    Views for getting details of an observation, posting updates for a new observation,
    or deleting an existing observation
    """
    def get(self, request, set_id):
        return JsonResponse({'observations': Observation.get_for_api(request.va)})

    def post(self, request, set_id):
        params = dict((key, val) for key, val in request.POST.items() if key in Observation.valid_fields())
        params['assignment'] = request.va
        params['user'] = request.annotator.user
        params['attribute'] = request.POST.getlist('attribute')
        params['measurables'] = request.POST.getlist('measurables')
        if 'animal_id' not in params:
            params['animal_id'] = Animal.objects.get(common_name__iexact=request.POST['animal_name']).id
        obs = Observation.create(**params)
        evt = obs.event_set.first()
        if request.va.status_id == 1:
            request.va.status_id = 2
            request.va.save()
        return JsonResponse({'observations': Observation.get_for_api(request.va), 'filename': evt.filename()})

    def delete(self, request, set_id):
        Observation.objects.filter(assignment=request.va).get(pk=request.GET.get('obs_id')).delete()
        return JsonResponse({'observations': Observation.get_for_api(request.va)})


class ObservationUpdate(APIView):
    """
    View for updating an existing assignment
    """
    def post(self, request, set_id, obs_id):
        obs = get_object_or_404(Observation, pk=obs_id, assignment=request.va)
        params = dict((key, val) for key, val in request.POST.items() if key in Observation.valid_fields())
        params['user'] = request.annotator.user
        params['updated_by'] = request.annotator

        if params.get('type', False) and obs.type != params['type']:
            return HttpResponseBadRequest('Not allowed to change Observation type')

        if obs.type == 'I':
            for key, val in params.items():
                setattr(obs, key, val)

        elif obs.type == 'A':
            animal_obs = obs.animalobservation
            for key, val in params.items():
                if key == 'user':
                    setattr(obs, 'user', val)
                    setattr(animal_obs, 'user', val)
                elif key in ['animal_id', 'sex', 'stage', 'length']:
                    setattr(animal_obs, key, val)
                else:
                    setattr(obs, key, val)

            animal_obs.save()

        obs.save()
        evt = obs.event_set.first()

        return JsonResponse({'observations': Observation.get_for_api(request.va), 'filename': evt.filename()})


class AnimalList(APIView):
    """
    Animal list view
    """
    def get(self, request, set_id):
        return JsonResponse({'animals': Animal.get_for_api(request.va)})


class AnimalDetail(APIView):
    """
    Animal detail view
    """
    def get(self, request, animal_id):
        return JsonResponse({'animal': get_object_or_404(Animal, pk=animal_id).to_json()})


class StatusUpdate(APIView):
    """
    Status update view (moves status to Ready for Review)
    """
    def post(self, request, set_id):
        request.va.status_id = 3
        request.va.save()
        return JsonResponse({'status': 'OK'})


class AcceptAssignment(APIView):
    """
    Accept assignment view (moves status to Accepted)
    """
    def post(self, request, set_id):
        if not request.annotator.is_lead():
            message = 'Assignment can only be Accepted by a lead'
        elif request.va.status_id != 3:
            message = 'Assignment must be Ready for Review to be Accepted'
        else:
            request.va.status_id = 4
            request.va.save()
            message = 'OK'
        return JsonResponse({'status': message})


class RejectAssignment(APIView):
    """
    Reject assignment view (moves status to Rejected)
    """
    def post(self, request, set_id):
        if not request.annotator.is_lead():
            message = 'Assignment can only be Rejected by a lead'
        elif request.va.status_id != 3:
            message = 'Assignment must be Ready for Review to be Rejected'
        else:
            request.va.status_id = 6
            request.va.save()
            message = 'OK'
        return JsonResponse({'status': message})


class ProgressUpdate(APIView):
    """
    Progress update view
    """
    def post(self, request, set_id):
        new_progress = request.va.update_progress(int(request.POST.get('progress')))
        return JsonResponse({'progress': new_progress})


class AttributeList(APIView):
    """
    Attribute (tag) list view
    """
    def get(self, request, set_id):
        return JsonResponse({'attributes': Attribute.tree_json(is_lead=request.annotator.is_lead(),
                                                               project=request.va.project)})


class Events(APIView):
    """
    Event views for creation and deletion
    """
    def post(self, request, set_id, obs_id):
        obs = get_object_or_404(Observation, pk=obs_id, assignment=request.va)
        params = dict((key, val) for key, val in request.POST.items() if key in Event.valid_fields())
        params['observation'] = obs
        params['user'] = request.annotator.user
        params['attribute'] = request.POST.getlist('attribute')
        params['measurables'] = request.POST.getlist('measurables')
        evt = Event.create(**params)
        return JsonResponse({'observations': Observation.get_for_api(request.va), 'filename': evt.filename()})

    def delete(self, request, set_id, obs_id):
        obs = get_object_or_404(Observation, pk=obs_id, assignment=request.va)
        evt = get_object_or_404(Event, pk=request.GET.get('evt_id'), observation=obs)
        evt.delete()
        if len(obs.event_set.all()) == 0:
            obs.delete()
        # TODO delete frame capture file
        return JsonResponse({'observations': Observation.get_for_api(request.va)})


class EventUpdate(APIView):
    """
    Event update view
    """
    def post(self, request, set_id, obs_id, evt_id):
        obs = get_object_or_404(Observation, pk=obs_id, assignment=request.va)
        evt = get_object_or_404(Event, pk=evt_id, observation=obs)
        params = dict((key, val) for key, val in request.POST.items()
                      if key in Event.valid_fields() and key not in ['extent', 'event_time'])
        params['user'] = request.annotator.user
        if 'measurables' in request.POST:
            measurable_values = request.POST.getlist('measurables')
            # todo: need to modify if there are other measurables than MaxN.. for now considering one element in list
            for measurable_value in measurable_values:
                if 'event_measurable_id' in request.POST:
                    # updating maxN valuse using pk of EventMeasurable object
                    event_measurable_id = int(request.POST['event_measurable_id'])
                    EventMeasurable(
                        id=event_measurable_id,
                        value=measurable_value,
                        event=evt,
                        measurable=Measurable(pk=MAXN_MEASURABLE_ID)
                    ).save(force_update=True)
                else:
                    # first time addition of maxN
                    EventMeasurable(
                        value=measurable_value,
                        event=evt,
                        measurable=Measurable(pk=MAXN_MEASURABLE_ID)
                    ).save()

        for key, val in params.items():
            if key != 'measurables':
                setattr(evt, key, val)

        evt.attribute = []
        for att_id in request.POST.getlist('attribute', []):
            evt.attribute.add(get_object_or_404(Attribute, pk=att_id))
        evt.save()
        filename = evt.filename()
        return JsonResponse({'observations': Observation.get_for_api(request.va), 'filename': filename})


class BulkEvents(APIView):
    date_format = '%b %d, %Y'
    time_format = '%H:%M'

    def get(self, request):
        result = {}

        min_date, max_date = None, None
        if 'min_date' in request.GET:
            min_date = dt.strptime(request.GET['min_date'], self.date_format)

        if 'max_date' in request.GET:
            max_date = dt.strptime(request.GET['max_date'], self.date_format)

        filter_params = {}
        if min_date and max_date:
            filter_params['last_modified_datetime__range'] = (min_date, max_date)
        elif min_date:
            filter_params['last_modified_datetime__gt'] = min_date
        elif max_date:
            filter_params['last_modified_datetime__lt'] = max_date

        for observation in Observation.objects.filter(**filter_params):
            assignment = observation.assignment
            video = assignment.video
            set_obj = video.set # named to avoid collision with python set()
            trip = set_obj.trip

            if trip.code not in result:
                result[trip.code] = self.make_trip_json(trip)
            trip_json = result[trip.code]

            if set_obj.code not in trip_json['sets']:
                trip_json['sets'][set_obj.code] = self.make_set_json(set_obj)

            set_json = trip_json['sets'][set_obj.code]

            video_name = str(video)
            if video_name not in set_json['videos']:
                set_json['videos'][video_name] = {
                    'video_name': video_name,
                    'observation': []
                }
            video_json = set_json['videos'][video_name]

            video_json['observation'].append({
                'organism': self.get_organism_json(observation),
                'observation_time': observation.observation_time,
                'duration': observation.duration,
                'events': [
                    {
                        'time': event.event_time,
                        'bounding_box': event.extent.wkt if event.extent else None,
                        'image_url': IMAGE_URL_FORMAT.format(
                            trip_code=trip.code,
                            set_code=set_obj.code,
                            obs_id=observation.id,
                            event_id=event.id
                        )
                    }
                    for event in observation.event_set.all()
                ]
            })

        return JsonResponse(result)

    def make_trip_json(self, trip):
        return {
            'trip_code': trip.code,
            'team': str(trip.team),
            'location': str(trip.location),
            'start_date': dt.strftime(trip.start_date, self.date_format),
            'end_date': dt.strftime(trip.end_date, self.date_format),
            'source': str(trip.source),
            'sets': {}
        }

    def make_set_json(self, set_obj):
        set_json = {
            'set_code': set_obj.code,
            'set_date': dt.strftime(set_obj.set_date, self.date_format),
            'drop_time': time.strftime(set_obj.drop_time, self.time_format),
            'latitude': float(set_obj.latitude),
            'longitude': float(set_obj.longitude),
            'depth': float(set_obj.depth),
            'reef': set_obj.reef().name,
            'habitat': str(set_obj.reef_habitat.habitat),
            'videos': {}
        }
        if set_obj.haul_date:
            set_json['haul_date'] = dt.strftime(set_obj.haul_date, self.date_format)
        if set_obj.haul_time:
            set_json['haul_time'] = time.strftime(set_obj.haul_time, self.time_format)

        return set_json

    def get_organism_json(self, observation):
        if hasattr(observation, 'animalobservation'):
            animal = observation.animal()
            return {
                'species': animal.species,
                'genus': animal.genus,
                'family': animal.family,
                'common_name': animal.common_name,
                'group': str(animal.group)
            }
        else:
            return None



class AffiliationList(APIView):
    """
    Affiliation list
    """

    def get(self, request):
        affiliations = Affiliation.objects.all().values('id', 'name')
        obj = {}
        for dictObj in affiliations:
            obj[dictObj['id']] = dictObj['name']
        return JsonResponse(obj)


class RestrictFilterChanges(View):
    """Restrict filter of Reef and Set
    changes in Trip Filter or Reef Filter restricts Sets
    changes in Trip Filter restricts Reef Filter
    changes in Reef Filter restricts Sets Filter"""

    def get(self, request):
        _dic = request.GET
        list_of_sets = []
        list_of_reefs = []

        if 'trip_id' in _dic:
            trip_id = _dic['trip_id']
        if 'reef_id' in _dic:
            reef_ids = _dic['reef_id']

        # if trip change
        if 'trip_id' in _dic and trip_id != '' and 'reef_id' not in _dic:
            trip = Trip.objects.filter(id=trip_id).order_by('code').all().prefetch_related('set_set')
            sites = Site.objects.filter(location_id=trip[0].location_id).order_by('name').all().prefetch_related(
                'reef_set')
            # find the code of each reef and remove those sets
            set_data = list(set(trip))[0].set_set
            for s in set_data.all():
                list_of_sets.append({"id": s.id, "code": s.code, "group": str(set_data.instance)})

            for s in sites:
                for r in s.reef_set.all():
                    list_of_reefs.append({"reef_group": str(s), "id": r.id, "name": r.name})
        # if reef changes
        elif 'reef_id' in _dic:
            if 'trip_id' in _dic and trip_id != '':
                sets = Set.objects.filter(trip_id=trip_id).filter(reef_habitat__reef_id=reef_ids)
            else:
                sets = Set.objects.filter(reef_habitat__reef_id=reef_ids)

            for each_set in list(set_utils(sets)):
                list_of_sets.append({"id": each_set.id, "code": each_set.code, "group": str(each_set.trip)})
        else:
            trip = Trip.objects.order_by('code').all().prefetch_related('set_set')
            sites = Site.objects.order_by('name').all().prefetch_related('reef_set')
            for trip_data in list(set(trip)):
                set_data = trip_data.set_set
                for s in set_data.all():
                    list_of_sets.append({"id": s.id, "code": s.code, "group": str(set_data.instance)})

            for s in sites:
                for r in s.reef_set.all():
                    list_of_reefs.append({"reef_group": str(s), "id": r.id, "name": r.name})

        if 'reef_id' not in _dic:
            return JsonResponse({'status': 'ok', "reefs": list_of_reefs, "sets": list_of_sets})
        else:
            return JsonResponse({'status': 'ok', "sets": list_of_sets})

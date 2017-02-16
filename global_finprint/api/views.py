from django.views.generic.base import View
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from ..trip.models import Trip
from ..annotation.models.animal import Animal
from ..annotation.models.video import Assignment
from ..annotation.models.observation import Observation, Attribute, Event
from ..core.models import FinprintUser


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

        if 'set_id' in kwargs:
            try:
                assignments = Assignment.get_all() if request.annotator.is_lead() \
                    else Assignment.get_active_for_annotator(request.annotator)
                request.va = assignments.get(pk=kwargs['set_id'])
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
            assignments = Assignment.get_active()
            if 'trip_id' in request.GET:
                assignments = assignments.filter(video__set__trip__id=request.GET.get('trip_id'))
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
        return JsonResponse({'observations': Observation.get_for_api(request.va)})


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
        for key, val in params.items():
            setattr(evt, key, val)
        evt.attribute = []
        for att_id in request.POST.getlist('attribute', []):
            evt.attribute.add(get_object_or_404(Attribute, pk=att_id))
        evt.save()
        return JsonResponse({'observations': Observation.get_for_api(request.va)})

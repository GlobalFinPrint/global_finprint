from django.views.generic.base import View
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseBadRequest
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from ..annotation.models import Annotator, VideoAnnotator, Observation, Animal, AnimalBehavior, ObservationFeature


class APIView(View):
    def dispatch(self, request, *args, **kwargs):
        if 'token' in request.GET:
            token = request.GET.get('token', None)
        elif 'token' in request.POST:
            token = request.POST.get('token', None)
        else:
            return HttpResponseForbidden()

        try:
            request.annotator = Annotator.objects.get(token=token)
        except Annotator.DoesNotExist:
            return HttpResponseForbidden()

        if 'set_id' in kwargs:
            try:
                request.va = VideoAnnotator.get_active_for_annotator(request.annotator).get(pk=kwargs['set_id'])
            except VideoAnnotator.DoesNotExist:
                return HttpResponseNotFound()

        return super().dispatch(request, *args, **kwargs)


class Login(View):
    def post(self, request):
        user = authenticate(
                username=request.POST.get('username', None),
                password=request.POST.get('password', None))

        if user is None:
            return HttpResponseForbidden()

        try:
            annotator = user.annotator
            token = annotator.set_token()
        except Annotator.DoesNotExist:
            return HttpResponseForbidden()

        va_list = list({'id': va.id, 'set_code': str(va.set()), 'file': str(va.video.file)} for va
                       in VideoAnnotator.get_active_for_annotator(annotator))

        return JsonResponse({'token': token, 'sets': va_list})


class Logout(APIView):
    def post(self, request):
        request.annotator.clear_token()
        return JsonResponse({'status': 'OK'})


class SetList(APIView):
    def get(self, request):
        va_list = list({'id': va.id, 'set_code': str(va.set()), 'file': str(va.video.file)} for va
                       in VideoAnnotator.get_active_for_annotator(request.annotator))
        return JsonResponse({'sets': va_list})


class SetDetail(APIView):
    def get(self, request, set_id):
        return JsonResponse({'set': {'id': request.va.id,
                                     'set_code': str(request.va.set()),
                                     'file': str(request.va.video.file),
                                     'observations': Observation.get_for_api(request.va),
                                     'animals': Animal.get_for_api(request.va),
                                     'behaviors': list(AnimalBehavior.objects.all().values()),
                                     'features': list(ObservationFeature.objects.all().values())}})


class Observations(APIView):
    def get(self, request, set_id):
        return JsonResponse({'observations': Observation.get_for_api(request.va)})

    def post(self, request, set_id):
        params = dict((key, val) for key, val in request.POST.items() if key in Observation.valid_fields())
        params['video_annotator'] = request.va
        params['user'] = request.annotator.user
        Observation.create(**params)
        request.va.status = 'I'
        request.va.save()
        return JsonResponse({'observations': Observation.get_for_api(request.va)})

    def delete(self, request, set_id):
        Observation.objects.filter(video_annotator=request.va).get(pk=request.GET.get('obs_id')).delete()
        return JsonResponse({'observations': Observation.get_for_api(request.va)})


class ObservationUpdate(APIView):
    def post(self, request, set_id, obs_id):
        obs = get_object_or_404(Observation, pk=obs_id, video_annotator=request.va)
        params = dict((key, val) for key, val in request.POST.items() if key in Observation.valid_fields())
        params['user'] = request.annotator.user

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
                elif key == 'behavior_ids':
                    setattr(animal_obs, 'behaviors', val.split(',') if val != '' else [])
                elif key == 'feature_ids':
                    setattr(animal_obs, 'features', val.split(',') if val != '' else [])
                elif key in ['animal_id', 'sex', 'stage', 'length', 'gear_on_animal',
                             'gear_fouled', 'tag', 'external_parasites']:
                    setattr(animal_obs, key, val)
                else:
                    setattr(obs, key, val)

            animal_obs.save()

        obs.save()
        return JsonResponse({'observations': Observation.get_for_api(request.va)})


class AnimalList(APIView):
    def get(self, request, set_id):
        return JsonResponse({'animals': Animal.get_for_api(request.va)})


class AnimalDetail(APIView):
    def get(self, request, animal_id):
        return JsonResponse({'animal': get_object_or_404(Animal, pk=animal_id).to_json()})


class BehaviorList(APIView):
    def get(self, request):
        return JsonResponse({'behaviors': list(AnimalBehavior.objects.all().values())})


class FeatureList(APIView):
    def get(self, request):
        return JsonResponse({'features': list(ObservationFeature.objects.all().values())})


class StatusUpdate(APIView):
    def post(self, request, set_id):
        request.va.status = 'R'
        request.va.save()
        return JsonResponse({'status': 'OK'})

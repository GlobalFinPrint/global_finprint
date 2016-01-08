from django.views.generic.base import View
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth import authenticate
from ..annotation.models import Annotator, VideoAnnotator, Observation


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

        return super().dispatch(request, *args, **kwargs)


class Login(View):
    def post(self, request):
        user = authenticate(
                username=request.POST.get('user', None),
                password=request.POST.get('password', None))

        if user is None:
            return HttpResponseForbidden()

        return JsonResponse({'token': user.annotator.set_token()})


class Logout(APIView):
    def post(self, request):
        request.annotator.clear_token()
        return JsonResponse({'status': 'OK'})


class SetList(APIView):
    def get(self, request):
        va_list = list({'id': va.id, 'file': str(va.video.file)} for va
                       in VideoAnnotator.objects.filter(annotator=request.annotator))
        return JsonResponse({'sets': va_list})


class SetDetail(APIView):
    def get(self, request, set_id):
        try:
            va = VideoAnnotator.objects.filter(annotator=request.annotator).get(pk=set_id)
            return JsonResponse({'set': {'id': va.id,
                                         'file': str(va.video.file),
                                         'observations': list(va.observation_set.all())}})
        except VideoAnnotator.DoesNotExist:
            return HttpResponseNotFound()


class Observations(APIView):
    def get(self, request, set_id):
        try:
            va = VideoAnnotator.objects.filter(annotator=request.annotator).get(pk=set_id)
            return JsonResponse({'observations': list(va.observation_set.all())})
        except VideoAnnotator.DoesNotExist:
            return HttpResponseNotFound()

    def post(self, request, set_id):
        try:
            va = VideoAnnotator.objects.filter(annotator=request.annotator).get(pk=set_id)
            params = dict((key, val) for key, val in request.POST if key in Observation._meta.get_all_field_names())
            params['video_annotator'] = va
            params['set'] = va.video.set
            params['user'] = request.annotator.user
            va.observation_set.create(**params)
            va.update(status='I')
            return JsonResponse({'observations': list(va.observation_set.all())})
        except VideoAnnotator.DoesNotExist:
            return HttpResponseNotFound()

    def delete(self, request, set_id):
        try:
            va = VideoAnnotator.objects.filter(annotator=request.annotator).get(pk=set_id)
            Observation.objects.filter(video_annotator=va).get(pk=request.GET.get('obs_id')).delete()
            return JsonResponse({'observations': list(va.observation_set.all())})
        except VideoAnnotator.DoesNotExist:
            return HttpResponseNotFound()


class AnimalList(APIView):
    def get(self, request, set_id):
        try:
            va = VideoAnnotator.objects.filter(annotator=request.annotator).get(pk=set_id)
            return JsonResponse({'animals': list(va.video.set.trip.region.animal_set.all().values())})
        except VideoAnnotator.DoesNotExist:
            return HttpResponseNotFound()


class StatusUpdate(APIView):
    def post(self, request, set_id):
        try:
            va = VideoAnnotator.objects.filter(annotator=request.annotator).get(pk=set_id)
            va.update(status='C')
            return JsonResponse({'status': 'OK'})
        except VideoAnnotator.DoesNotExist:
            return HttpResponseNotFound()

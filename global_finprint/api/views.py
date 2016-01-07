from django.views.generic.base import View
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotFound
from django.contrib.auth import authenticate
from ..annotation.models import Annotator, VideoAnnotator


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
        set_list = list({'id': set.id, 'file': str(set.video.file)} for set
                        in VideoAnnotator.objects.filter(annotator=request.annotator))
        return JsonResponse({'sets': set_list})


class SetDetail(APIView):
    def get(self, request, set_id):
        try:
            set = VideoAnnotator.objects.filter(annotator=request.annotator).get(pk=set_id)
            return JsonResponse({'set': {'id': set.id,
                                         'file': str(set.video.file),
                                         'observations': list(set.observation_set.all())}})
        except VideoAnnotator.DoesNotExist:
            return HttpResponseNotFound()


class Observation(APIView):
    def get(self, request, set_id):
        try:
            set = VideoAnnotator.objects.filter(annotator=request.annotator).get(pk=set_id)
            return JsonResponse({'observations': list(set.observation_set.all())})
        except VideoAnnotator.DoesNotExist:
            return HttpResponseNotFound()

    def post(self, request, set_id):
        try:
            set = VideoAnnotator.objects.filter(annotator=request.annotator).get(pk=set_id)
            return JsonResponse({})  # TODO
        except VideoAnnotator.DoesNotExist:
            return HttpResponseNotFound()

    def delete(self, request, set_id):
        try:
            set = VideoAnnotator.objects.filter(annotator=request.annotator).get(pk=set_id)
            return JsonResponse({})  # TODO
        except VideoAnnotator.DoesNotExist:
            return HttpResponseNotFound()


class AnimalList(APIView):
    def get(self, request, set_id):
        try:
            set = VideoAnnotator.objects.filter(annotator=request.annotator).get(pk=set_id)
            return JsonResponse({'animals': list(set.video.set.trip.region.animal_set.all().values())})
        except VideoAnnotator.DoesNotExist:
            return HttpResponseNotFound()


class StatusUpdate(APIView):
    def post(self, request, set_id):
        try:
            set = VideoAnnotator.objects.filter(annotator=request.annotator).get(pk=set_id)
            return JsonResponse({})  # TODO
        except VideoAnnotator.DoesNotExist:
            return HttpResponseNotFound()

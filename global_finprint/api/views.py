from django.views.generic.base import View
from django.http import JsonResponse, HttpResponseForbidden
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
        set_list = list(VideoAnnotator.objects.filter(annotator=request.annotator).values('id', 'video__file'))
        return JsonResponse({'sets': set_list})


class SetDetail(APIView):
    def get(self, request, set_id):
        set = VideoAnnotator.objects.filter(annotator=request.annotator).get(pk=set_id)
        return JsonResponse({'set': {'id': set.id,
                                     'file': str(set.video.file),
                                     'observations': list(set.observation_set.all())
                                     }
                             })


class Observation(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass

    def delete(self, request):
        pass


class AnimalList(APIView):
    def get(self, request):
        pass


class StatusUpdate(APIView):
    def post(self, request):
        pass

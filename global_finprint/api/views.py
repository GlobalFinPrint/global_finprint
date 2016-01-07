from django.views.generic.base import View
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate
from ..annotation.models import Annotator


class APIView(View):
    def dispatch(self, request, *args, **kwargs):
        if 'token' in request.GET:
            token = request.GET.get('token', None)
        elif 'token' in request.POST:
            token = request.POST.get('token', None)
        else:
            return HttpResponseForbidden()

        try:
            request.user = Annotator.objects.get(token=token).user
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
        return JsonResponse({'user': request.user.username})


class SetList(APIView):
    def get(self, request):
        pass


class SetDetail(APIView):
    def get(self, request, set_id):
        pass


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

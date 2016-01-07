from django.views.generic.base import View
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate


class APIView(View):
    def dispatch(self, request, *args, **kwargs):
        # TODO error without user token
        super().dispatch(request, *args, **kwargs)


class APIResponse(JsonResponse):
    def __init__(self, data):
        # TODO add to data
        super().__init__(data)


class Login(View):
    def post(self, request):
        user = authenticate(
                user=self.request.POST.get('user', None),
                password=self.request.POST.get('password', None))

        if user is None:
            return HttpResponseForbidden()

        annotator = user.annotator



class Logout(APIView):
    def post(self, request):
        pass


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

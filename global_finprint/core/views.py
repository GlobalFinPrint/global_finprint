from django.views.generic.base import View
from django.shortcuts import redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import FinprintUser

class UrlRedirect(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return redirect('home', permanent=True)

    @staticmethod
    def post(request, *args, **kwargs):
        return redirect('home', permanent=True)

    @staticmethod
    def put(request, *args, **kwargs):
        return redirect('home', permanent=True)

    @staticmethod
    def delete(request, *args, **kwargs):
        return redirect('home', permanent=True)


class UserInfoView(View):
    def get(self, request, id):
        user = get_object_or_404(FinprintUser, pk=id)
        return JsonResponse(user.to_json())

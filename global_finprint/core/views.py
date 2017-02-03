from django.views.generic.base import View
from django.shortcuts import redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import FinprintUser


class UrlRedirect(View):
    """
    Helper methods for redirection
    """
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
    """
    User info view to power popover
    """
    def get(self, request, id):
        user = get_object_or_404(FinprintUser, pk=id)
        json = user.to_json()
        json['content'] = '{0} observations submit in {1} assignments ({2} active)' \
            .format(len(json['observations']), len(json['assignments']), len(user.active_assignments()))
        return JsonResponse(json)

from django.views.generic.base import View
from django.shortcuts import redirect


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

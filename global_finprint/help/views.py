from django.views.generic import View
from django.shortcuts import render


class WebHelpView(View):
    template = 'pages/help/web_help.html'

    def get(self, request):
        return render(request, self.template)


class ClientHelpView(View):
    template = 'pages/help/client_help.html'

    def get(self, request):
        return render(request, self.template)

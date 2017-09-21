from django.views.generic import RedirectView
from django.contrib.staticfiles.templatetags.staticfiles import static


class WebHelpView(RedirectView):
    permanent = True
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        return static('pdf/Finprint Website User Guide.pdf')


class ClientHelpView(RedirectView):
    permanent = True
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        return static('pdf/Finprint Annotator User Guide.pdf')

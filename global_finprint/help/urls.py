from django.conf.urls import url
from .views import WebHelpView, ClientHelpView

urlpatterns = [
    url(r"web/$", WebHelpView.as_view(), name="web_help"),
    url(r"client/$", ClientHelpView.as_view(), name="client_help"),
    ]

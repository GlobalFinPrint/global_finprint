from django.conf.urls import url
from ..views.environmentmeasure import *


urlpatterns = [
    url(r"^create/$", EnvironmentMeasureCreateView.as_view(), name='environmentmeasure_create'),
    url(r"^(?P<pk>\d+)/$", EnvironmentMeasureUpdateView.as_view(), name='environmentmeasure_update'),
]

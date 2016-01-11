from django.conf.urls import url

from global_finprint.annotation.views.observations import *

urlpatterns = [
    url(r"", ObservationListView.as_view(), name='set_observation_list'),
]

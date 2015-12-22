from django.conf.urls import url

from global_finprint.annotation.views.observations import *

urlpatterns = [
    url(r"^create/$", ObservationCreateView.as_view(), name='observation_create'),
    url(r"^(?P<pk>\d+)/$", ObservationUpdateView.as_view(), name='observation_update'),

    url(r"", ObservationListView.as_view(), name='set_observation_list'),
]

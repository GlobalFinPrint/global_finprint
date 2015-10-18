from django.conf.urls import url
from global_finprint.bruv.views import *

urlpatterns = [
    # url(r"^(?P<set_pk>\d+)/observations/$", ObservationListView.as_view(), name='set_observations_list'),

    url(r"", ObservationListView.as_view(), name='set_observations_list'),
]

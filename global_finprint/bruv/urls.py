from django.conf.urls import patterns, url
from .views import *

urlpatterns = [
    url(r"^create/$", SetCreateView.as_view(), name='set_create'),

    url(r"^(?P<set_pk>\d+)/observations/$", ObservationListView.as_view(), name='set_observations_list'),
    url(r"^(?P<pk>\d+)/$", SetUpdateView.as_view(), name='set_update'),
]

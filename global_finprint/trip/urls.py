from django.conf.urls import patterns, url
from global_finprint.bruv.views import SetListView
from .views import *

urlpatterns =[
    url(r"^create/$", TripCreateView.as_view(), name='trip_create'),

    url(r"(?P<trip_pk>\d+)/sets/$", SetListView.as_view(), name='trip_set_list'),
    url(r"(?P<pk>\d+)/$", TripUpdateView.as_view(), name='trip_update'),

    url(r"", TripListView.as_view(), name='trip_list'),
]

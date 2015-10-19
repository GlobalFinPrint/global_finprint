from django.conf.urls import include, url
from .views import *


urlpatterns =[
    url(r"(?P<trip_pk>\d+)/sets/", include('global_finprint.bruv.urls.sets')),

    url(r"^create/$", TripCreateView.as_view(), name='trip_create'),
    url(r"(?P<pk>\d+)/$", TripUpdateView.as_view(), name='trip_update'),

    url(r"", TripListView.as_view(), name='trip_list'),
]

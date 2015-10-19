from django.conf.urls import url

from global_finprint.trip.views import trip_detail
from global_finprint.bruv.views.sets import set_detail
from global_finprint.bruv.views.observations import observation_detail


urlpatterns = [
    url(r"^trips/(?P<pk>\d+)/$", trip_detail, name='api_trip_detail'),
    url(r"^sets/(?P<pk>\d+)/$", set_detail, name='api_set_detail'),
    url(r"^observations/(?P<pk>\d+)/$", observation_detail, name='api_observation_detail'),
]
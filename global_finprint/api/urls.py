from django.conf.urls import url

from ..trip.views import trip_detail, trip_sets_geojson
from ..bruv.views.sets import set_detail
from ..habitat.views import reef_detail_geojson
from ..bruv.views.observations import observation_detail, observation_post
from ..bruv.views.annotation import site_animal_list, annotator_video_list


urlpatterns = [
    # object details
    url(r"^trips/(?P<pk>\d+)/$", trip_detail, name='api_trip_detail'),
    url(r"^sets/(?P<pk>\d+)/$", set_detail, name='api_set_detail'),
    url(r"^observations/(?P<pk>\d+)/$", observation_detail, name='api_observation_detail'),

    # geo
    url(r"^reef/(?P<reef_id>\d+)/geojson/$", reef_detail_geojson, name='api_reef_detail_geojson'),
    url(r"^trip/(?P<trip_id>\d+)/sets/geojson/$", trip_sets_geojson, name='api_trip_sets_geojson'),

    # annotation
    url(r"^observation/$", observation_post, name='api_observation_post'),
    url(r"^annotation/animals/(?P<site_id>\d+)/$", site_animal_list, name='api_animal_list_by_site'),
    url(r"^annotation/videos/(?P<annotator_id>\d+)/$", annotator_video_list, name='api_video_list_by_annotator'),
]
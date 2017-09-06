from django.conf.urls import url
from global_finprint.habitat.views import reef_detail_geojson
from global_finprint.trip.views import trip_sets_geojson
from global_finprint.report.views import planned_site_geojson

urlpatterns = [

    ######
    # geo -- (only the trip map is used at this time)
    url(r"^reef/(?P<reef_id>\d+)/geojson/$", reef_detail_geojson, name='api_reef_detail_geojson'),
    url(r"^trip/(?P<trip_id>\d+)/sets/geojson/$", trip_sets_geojson, name='api_trip_sets_geojson'),
    url(r"^report/status/geojson/$", planned_site_geojson, name='api_planned_site_geojson'),

]

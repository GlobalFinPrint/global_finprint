from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from global_finprint.annotation.views.annotation import site_animal_list, annotator_video_list
from global_finprint.annotation.views.observations import observation_post
from ..habitat.views import reef_detail_geojson
from ..trip.views import trip_sets_geojson
from ..report.views import planned_site_geojson
from global_finprint.api import views
from global_finprint.api.views import RestrictFilterChanges


urlpatterns = [
    # geo
    url(r"^reef/(?P<reef_id>\d+)/geojson/$", reef_detail_geojson, name='api_reef_detail_geojson'),
    url(r"^trip/(?P<trip_id>\d+)/sets/geojson/$", trip_sets_geojson, name='api_trip_sets_geojson'),
    url(r"^report/status/geojson/$", planned_site_geojson, name='api_planned_site_geojson'),

    # annotation
    url(r"^observation/$", observation_post, name='api_observation_post'),
    url(r"^annotation/animals/(?P<site_id>\d+)/$", site_animal_list, name='api_animal_list_by_site'),
    url(r"^annotation/videos/(?P<annotator_id>\d+)/$", annotator_video_list, name='api_video_list_by_annotator'),

    # annotation tool api
    url(r"^login$", csrf_exempt(views.Login.as_view()), name='api_login'),
    url(r"^logout$", csrf_exempt(views.Logout.as_view()), name='api_logout'),
    url(r"^trip$", csrf_exempt(views.TripList.as_view()), name='api_trip_list'),
    url(r"^set$", csrf_exempt(views.SetList.as_view()), name='api_set_list'),
    url(r"^set/(?P<set_id>\d+)/attributes$", csrf_exempt(views.AttributeList.as_view()), name='api_attribute_list'),
    url(r"^set/(?P<set_id>\d+)$", csrf_exempt(views.SetDetail.as_view()), name='api_set_detail'),
    url(r"^set/(?P<set_id>\d+)/obs$", csrf_exempt(views.Observations.as_view()), name='api_observation'),
    url(r"^set/(?P<set_id>\d+)/obs/(?P<obs_id>\d+)$", csrf_exempt(views.ObservationUpdate.as_view()),
        name='api_observation_update'),
    url(r"^set/(?P<set_id>\d+)/animals$", csrf_exempt(views.AnimalList.as_view()), name='api_animal_list'),
    url(r"^set/(?P<set_id>\d+)/done$", csrf_exempt(views.StatusUpdate.as_view()), name='api_status_update'),
    url(r"^set/(?P<set_id>\d+)/accept", csrf_exempt(views.AcceptAssignment.as_view()), name='api_accept_assign'),
    url(r"^set/(?P<set_id>\d+)/reject", csrf_exempt(views.RejectAssignment.as_view()), name='api_reject_assign'),
    url(r"^set/(?P<set_id>\d+)/progress$", csrf_exempt(views.ProgressUpdate.as_view()), name='api_progress_update'),
    url(r"^animal/(?P<animal_id>\d+)$", csrf_exempt(views.AnimalDetail.as_view()), name='api_animal_detail'),
    url(r"^set/(?P<set_id>\d+)/obs/(?P<obs_id>\d+)/event$", csrf_exempt(views.Events.as_view()), name='api_events'),
    url(r"^set/(?P<set_id>\d+)/obs/(?P<obs_id>\d+)/event/(?P<evt_id>\d+)$",
        csrf_exempt(views.EventUpdate.as_view()), name='api_event_update'),
    url(r"^annotator", csrf_exempt(views.AnnotatorList.as_view()), name='api_annotator_list'),
    url(r"^affiliations", csrf_exempt(views.AffiliationList.as_view()), name='api_affiliation_list'),
    url(r"^restrict_filter_dropdown$", csrf_exempt(views.RestrictFilterChanges.as_view()), name='restrict_filter_dropdown'),
]

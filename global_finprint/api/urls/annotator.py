from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from global_finprint.api.views import annotator

urlpatterns = [

    ######
    # annotation tool api
    # access
    url(r"^login$", csrf_exempt(annotator.Login.as_view()), name='api_login'),
    url(r"^logout$", csrf_exempt(annotator.Logout.as_view()), name='api_logout'),

    # assignments
    url(r"^set$", csrf_exempt(annotator.SetList.as_view()), name='api_set_list'),

    # set details and list restrictions based on region / project
    url(r"^set/(?P<set_id>\d+)$", csrf_exempt(annotator.SetDetail.as_view()), name='api_set_detail'),
    url(r"^set/(?P<set_id>\d+)/attributes$", csrf_exempt(annotator.AttributeList.as_view()), name='api_attribute_list'),
    url(r"^set/(?P<set_id>\d+)/animals$", csrf_exempt(annotator.AnimalList.as_view()), name='api_animal_list'),

    # reading and writing obs and events
    url(r"^set/(?P<set_id>\d+)/obs$", csrf_exempt(annotator.Observations.as_view()), name='api_observation'),
    url(r"^set/(?P<set_id>\d+)/obs/(?P<obs_id>\d+)$", csrf_exempt(annotator.ObservationUpdate.as_view()),
        name='api_observation_update'),
    url(r"^set/(?P<set_id>\d+)/obs/(?P<obs_id>\d+)/event$", csrf_exempt(annotator.Events.as_view()), name='api_events'),
    url(r"^set/(?P<set_id>\d+)/obs/(?P<obs_id>\d+)/event/(?P<evt_id>\d+)$",
        csrf_exempt(annotator.EventUpdate.as_view()), name='api_event_update'),

    url(r"^animal/(?P<animal_id>\d+)$", csrf_exempt(annotator.AnimalDetail.as_view()), name='api_animal_detail'),

    # progress
    url(r"^set/(?P<set_id>\d+)/done$", csrf_exempt(annotator.StatusUpdate.as_view()), name='api_status_update'),
    url(r"^set/(?P<set_id>\d+)/accept", csrf_exempt(annotator.AcceptAssignment.as_view()), name='api_accept_assign'),
    url(r"^set/(?P<set_id>\d+)/reject", csrf_exempt(annotator.RejectAssignment.as_view()), name='api_reject_assign'),
    url(r"^set/(?P<set_id>\d+)/progress$", csrf_exempt(annotator.ProgressUpdate.as_view()), name='api_progress_update'),

    # for assignment filters
    url(r"^trip$", csrf_exempt(annotator.TripList.as_view()), name='api_trip_list'),
    url(r"^annotator", csrf_exempt(annotator.AnnotatorList.as_view()), name='api_annotator_list'),
    url(r"^affiliations", csrf_exempt(annotator.AffiliationList.as_view()), name='api_affiliation_list'),
    url(r"^restrict_filter_dropdown$", csrf_exempt(annotator.RestrictFilterChanges.as_view()),
        name='restrict_filter_dropdown'),

]

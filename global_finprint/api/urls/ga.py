from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from global_finprint.api.views import annotator

# for Global Archive and Event Measure (incl. EMIOlib)
urlpatterns = [

    # fetch the observations for an assignment or master record
    url(r"^assignment/(?P<assignment_id>\d+)/obs$", csrf_exempt(annotator.Observations.as_view()), name='api_assignment_observation'),
    url(r"^master/(?P<master_record_id>\d+)/obs$", csrf_exempt(annotator.Observations.as_view()), name='api_master_observation'),
]

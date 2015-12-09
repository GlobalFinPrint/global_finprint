from django.conf.urls import include, url
from ..views.sets import *


urlpatterns = [
    url(r"^(?P<set_pk>\d+)/observations/", include('global_finprint.bruv.urls.observations')),
    url(r"^(?P<set_pk>\d+)/$", SetListView.as_view(), name='set_update'),
    url(r"", SetListView.as_view(), name='trip_set_list'),
]

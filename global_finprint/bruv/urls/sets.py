from django.conf.urls import include, url
from ..views.sets import *


urlpatterns = [
    url(r"^(?P<set_pk>\d+)/observations/", include('global_finprint.bruv.urls.observations')),

    url(r"^create/$", SetCreateView.as_view(), name='set_create'),
    url(r"^(?P<pk>\d+)/$", SetUpdateView.as_view(), name='set_update'),

    url(r"", SetListView.as_view(), name='trip_set_list'),
]

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from global_finprint.annotation.views.observations import *

urlpatterns = [
    url(r"^$", ObservationListView.as_view(), name='set_observation_list'),
    url(r"^edit_data/(?P<evt_id>\d+)$", csrf_exempt(ObservationEditData.as_view()), name='observation_edit_data'),
    url(r"^save_data/(?P<evt_id>\d+)$", csrf_exempt(ObservationSaveData.as_view()), name='observation_save_data'),
]

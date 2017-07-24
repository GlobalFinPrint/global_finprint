from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from global_finprint.annotation.views.compare import GetMasterView
from global_finprint.annotation.views.observations import MasterObservationEditEvent, \
    MasterObservationSaveEvent, MasterObservationListView, ManageMasterView, \
    MasterObservationDeleteEvent


urlpatterns = [
    url(r"^(?P<set_id>\d+)$", csrf_exempt(GetMasterView.as_view()), name='get_master'),

    url(r"^review/(?P<master_id>\d+)$", MasterObservationListView.as_view(), name='master_review'),
    url(r"^manage/(?P<master_id>\d+)$", ManageMasterView.as_view(), name='master_manage'),

    url(r"^(?P<set_id>\d+)/observation/edit/(?P<evt_id>\d+)$", csrf_exempt(MasterObservationEditEvent.as_view()),
        name='master_edit_obs'),
    url(r"^(?P<set_id>\d+)/observation/save/(?P<evt_id>\d+)$", csrf_exempt(MasterObservationSaveEvent.as_view()),
        name='master_save_obs'),
    url(r"^(?P<set_id>\d+)/observation/delete/(?P<evt_id>\d+)$", csrf_exempt(MasterObservationDeleteEvent.as_view()),
        name='master_delete_obs'),
]

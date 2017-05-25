from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from global_finprint.annotation.views.compare import GetMasterView
from global_finprint.annotation.views.observations import MasterObservationEditData, \
    MasterObservationSaveData, EditMeasurablesInline, MasterObservationListView, ManageMasterView


urlpatterns = [
    url(r"^(?P<set_id>\d+)$", csrf_exempt(GetMasterView.as_view()), name='get_master'),

    url(r"^review/(?P<master_id>\d+)$", MasterObservationListView.as_view(), name='master_review'),
    url(r"^manage/(?P<master_id>\d+)$", ManageMasterView.as_view(), name='master_manage'),

    url(r"^master/(?P<set_id>\d+)/edit_data/(?P<evt_id>\d+)$", csrf_exempt(MasterObservationEditData.as_view()),
        name='master_edit_obs'),
    url(r"^master/(?P<set_id>\d+)/save_data/(?P<evt_id>\d+)$", csrf_exempt(MasterObservationSaveData.as_view()),
        name='master_save_obs'),

    url(r"^master/edit_measurables/(?P<evt_id>\d+)$", csrf_exempt(EditMeasurablesInline.as_view()),
        name='edit_measurables_inline')
]

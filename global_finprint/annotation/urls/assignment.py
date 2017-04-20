from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from global_finprint.annotation.views.assignment import VideoAutoAssignView, AssignmentManageView, \
    AssignmentListView, AssignmentListTbodyView, AssignmentModalBodyView, UnassignModalBodyView
from global_finprint.annotation.views.compare import AssignmentCompareView, AssignmentDetailView, \
    GetMasterView, MasterReviewView, MasterSetCompleted, MasterSetDeprecated
from global_finprint.annotation.views.observations import MasterObservationEditData, \
    MasterObservationSaveData, EditMeasurablesInline

urlpatterns = [
    url(r"^$", AssignmentListView.as_view(), name='assignment_list'),
    url(r"^search$", AssignmentListTbodyView.as_view(), name='assignment_search'),
    url(r"^manage/(?P<assignment_id>\d+)$", AssignmentManageView.as_view(), name='assignment_manage'),
    url(r"^modal/(?P<set_id>\d+)$", AssignmentModalBodyView.as_view(), name='assignment_modal'),
    url(r"^unassign_modal/(?P<assignment_id>\d+)$", UnassignModalBodyView.as_view(), name='unassign_modal'),
    url(r"^auto$", VideoAutoAssignView.as_view(), name='auto_assign'),
    url(r"^compare/(?P<set_id>\d+)$", AssignmentCompareView.as_view(), name='assignment_compare'),
    url(r"^review/(?P<master_id>\d+)$", MasterReviewView.as_view(), name='master_review'),
    url(r"^detail/(?P<assignment_id>\d+)$", AssignmentDetailView.as_view(), name='get_assignment_detail'),
    url(r"^master/(?P<set_id>\d+)$", csrf_exempt(GetMasterView.as_view()), name='get_master'),
    url(r"^master/(?P<set_id>\d+)/edit_data/(?P<evt_id>\d+)$", csrf_exempt(MasterObservationEditData.as_view()),
        name='master_edit_obs'),
    url(r"^master/(?P<set_id>\d+)/save_data/(?P<evt_id>\d+)$", csrf_exempt(MasterObservationSaveData.as_view()),
        name='master_save_obs'),
    url(r"^master/(?P<master_id>\d+)/complete$", csrf_exempt(MasterSetCompleted.as_view()),
        name='master_set_completed'),
    url(r"^master/(?P<master_id>\d+)/deprecate$", csrf_exempt(MasterSetDeprecated.as_view()),
        name='master_set_deprecated'),
    url(r"^master/edit_measurables/(?P<evt_id>\d+)$", csrf_exempt(EditMeasurablesInline.as_view()),
        name='edit_measurables_inline')
]

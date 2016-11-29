from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from global_finprint.annotation.views.assignment import VideoAutoAssignView, AssignmentManageView, \
    AssignmentListView, AssignmentListTbodyView, AssignmentModalBodyView
from global_finprint.annotation.views.compare import AssignmentCompareView, AssignmentDetailView, \
    GetMasterView, MasterReviewView, MasterSetCompleted, MasterSetDeprecated

urlpatterns = [
    url(r"^$", AssignmentListView.as_view(), name='assignment_list'),
    url(r"^search$", AssignmentListTbodyView.as_view(), name='assignment_search'),
    url(r"^manage/(?P<assignment_id>\d+)$", AssignmentManageView.as_view(), name='assignment_manage'),
    url(r"^modal/(?P<set_id>\d+)$", AssignmentModalBodyView.as_view(), name='assignment_modal'),
    url(r"^auto$", VideoAutoAssignView.as_view(), name='auto_assign'),
    url(r"^compare/(?P<set_id>\d+)$", AssignmentCompareView.as_view(), name='assignment_compare'),
    url(r"^review/(?P<master_id>\d+)$", MasterReviewView.as_view(), name='master_review'),
    url(r"^detail/(?P<assignment_id>\d+)$", AssignmentDetailView.as_view(), name='get_assignment_detail'),
    url(r"^master/(?P<set_id>\d+)$", csrf_exempt(GetMasterView.as_view()), name='get_master'),
    url(r"^master/(?P<master_id>\d+)/complete$", csrf_exempt(MasterSetCompleted.as_view()), name='master_set_completed'),
    url(r"^master/(?P<master_id>\d+)/deprecate$", csrf_exempt(MasterSetDeprecated.as_view()), name='master_set_deprecated'),
]

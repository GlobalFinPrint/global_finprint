from django.conf.urls import url, include

from global_finprint.annotation.views.assignment import VideoAutoAssignView, AssignmentManageView, \
    AssignmentListView, AssignmentListTbodyView, AssignmentModalBodyView, UnassignModalBodyView
from global_finprint.annotation.views.compare import AssignmentCompareView, AssignmentDetailView


urlpatterns = [
    url(r"^$", AssignmentListView.as_view(), name='assignment_list'),
    url(r"^search$", AssignmentListTbodyView.as_view(), name='assignment_search'),
    url(r"^manage/(?P<assignment_id>\d+)$", AssignmentManageView.as_view(), name='assignment_manage'),

    url(r"^modal/(?P<set_id>\d+)$", AssignmentModalBodyView.as_view(), name='assignment_modal'),
    url(r"^unassign_modal/(?P<assignment_id>\d+)$", UnassignModalBodyView.as_view(), name='unassign_modal'),
    url(r"^auto$", VideoAutoAssignView.as_view(), name='auto_assign'),

    url(r"^detail/(?P<assignment_id>\d+)$", AssignmentDetailView.as_view(), name='get_assignment_detail'),

    url(r"^compare/(?P<set_id>\d+)$", AssignmentCompareView.as_view(), name='assignment_compare'),

    url(r"^master/", include('global_finprint.annotation.urls.master')),
]

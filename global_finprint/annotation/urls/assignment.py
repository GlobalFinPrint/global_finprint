from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from global_finprint.annotation.views.assignment import VideoAutoAssignView, ManageAssignmentView, ObservationListView, \
    AssignmentListView, AssignmentListTbodyView, AssignmentModalBodyView, UnassignModalBodyView, AssignMultipleVideosModel,\
    AssignMultipleVideoToAnnotators
from global_finprint.annotation.views.compare import AssignmentCompareView, AssignmentDetailView


urlpatterns = [
    url(r"^$", AssignmentListView.as_view(), name='assignment_list'),
    url(r"^search$", AssignmentListTbodyView.as_view(), name='assignment_search'),
    url(r"^review/(?P<assignment_id>\d+)$", ObservationListView.as_view(), name='assignment_review'),
    url(r"^manage/(?P<assignment_id>\d+)$", ManageAssignmentView.as_view(), name='assignment_manage'),

    url(r"^modal/(?P<set_id>\d+)$", AssignmentModalBodyView.as_view(), name='assignment_modal'),
    url(r"^unassign_modal/(?P<assignment_id>\d+)$", UnassignModalBodyView.as_view(), name='unassign_modal'),
    url(r"^auto$", VideoAutoAssignView.as_view(), name='auto_assign'),

    url(r"^detail/(?P<assignment_id>\d+)$", AssignmentDetailView.as_view(), name='get_assignment_detail'),

    url(r"^compare/(?P<set_id>\d+)$", AssignmentCompareView.as_view(), name='assignment_compare'),

    url(r"^master/", include('global_finprint.annotation.urls.master')),

    url(r"^assign_selected_videos$",  csrf_exempt(AssignMultipleVideosModel.as_view()),
        name='assign_selected_videos'),
    url(r"^save_multi_video_assignment$", csrf_exempt(AssignMultipleVideoToAnnotators.as_view()),
        name='multi_video_assignment')
]

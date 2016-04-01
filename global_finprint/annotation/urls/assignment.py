from django.conf.urls import url
from global_finprint.annotation.views.assignment import \
    VideoAnnotatorListView, RemoveVideoAnnotatorView, DisableVideoAnnotatorView, \
    EnableVideoAnnotatorView, VideoAnnotatorJSONListView, VideoAnnotatorSelectTripView, \
    VideoAutoAssignView, AssignmentManageView, AssignmentListView, AssignmentListTbodyView

urlpatterns = [
    # url(r"^$", VideoAnnotatorSelectTripView.as_view(), name='video_annotator_select_trip'),
    # url(r"^(?P<trip_id>\d+)$", VideoAnnotatorListView.as_view(), name='video_annotator_list'),
    # url(r"^auto/(?P<ids>\d+_\d+)$", VideoAutoAssignView.as_view(), name='video_auto_assign'),
    # url(r"^remove/$", RemoveVideoAnnotatorView.as_view(), name='remove_video_annotator'),
    # url(r"^disable/$", DisableVideoAnnotatorView.as_view(), name='disable_video_annotator'),
    # url(r"^enable/$", EnableVideoAnnotatorView.as_view(), name='disable_video_annotator'),
    # url(r"^list/$", VideoAnnotatorJSONListView.as_view(), name='video_annotator_json_list'),
    url(r"^$", AssignmentListView.as_view(), name='assignment_list'),
    url(r"^search$", AssignmentListTbodyView.as_view(), name='assignment_search'),
    url(r"^manage/(?P<assignment_id>\d+)$", AssignmentManageView.as_view(), name='assignment_manage')
]

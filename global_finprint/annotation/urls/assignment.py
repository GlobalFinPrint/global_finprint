from django.conf.urls import url
from global_finprint.annotation.views.assignment import \
    VideoAnnotatorListView, RemoveVideoAnnotatorView, DisableVideoAnnotatorView, \
    EnableVideoAnnotatorView, VideoAnnotatorJSONListView

urlpatterns = [
    url(r"^$", VideoAnnotatorListView.as_view(), name='video_annotator_list'),
    url(r"^remove/$", RemoveVideoAnnotatorView.as_view(), name='remove_video_annotator'),
    url(r"^disable/$", DisableVideoAnnotatorView.as_view(), name='disable_video_annotator'),
    url(r"^enable/$", EnableVideoAnnotatorView.as_view(), name='disable_video_annotator'),
    url(r"^list/$", VideoAnnotatorJSONListView.as_view(), name='video_annotator_json_list'),
]

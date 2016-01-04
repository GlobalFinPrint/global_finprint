from django.conf.urls import url
from global_finprint.annotation.views.assignment import VideoAnnotatorListView

urlpatterns = [
    url(r"", VideoAnnotatorListView.as_view(), name='video_annotator_list'),
]

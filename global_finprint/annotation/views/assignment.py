from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from ..models import VideoAnnotator
from ..forms import VideoAnnotatorForm


class VideoAnnotatorListView(CreateView):
    model = VideoAnnotator
    form_class = VideoAnnotatorForm
    context_object_name = 'video_annotator'
    template_name = 'pages/annotation/video_annotator_list.html'
    success_msg = 'Video annotator assigned'
    success_url = reverse_lazy('video_annotator_list')

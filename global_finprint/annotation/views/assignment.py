from django.views.generic import CreateView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from ..models import VideoAnnotator, Video
from ..forms import VideoAnnotatorForm


class VideoAnnotatorListView(CreateView):
    model = VideoAnnotator
    form_class = VideoAnnotatorForm
    context_object_name = 'video_annotator'
    template_name = 'pages/annotation/video_annotator_list.html'
    success_msg = 'Video annotator assigned'
    success_url = reverse_lazy('video_annotator_list')

    def form_invalid(self, form):
        messages.error(self.request, 'Form errors found')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.all()
        return context

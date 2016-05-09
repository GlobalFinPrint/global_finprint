from django.db import models

from global_finprint.core.models import AuditableModel, FinprintUser


# todo:  pull video file names into ranked list (for l & r, etc.)
class Video(AuditableModel):
    file = models.CharField(max_length=100, null=True, blank=True)

    def annotators_assigned(self):
        return list(a.annotator for a in self.assignment_set.all())

    def __str__(self):
        return u"{0}".format(self.file)


# 1 = Not Started, 2 = In progress, 3 = Ready for review
# 4 = Completed, 5 = Disabled, 6 = Rejected
class AnnotationState(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return u'{0}'.format(self.name)

    class Meta:
        ordering = ['id']


class Assignment(AuditableModel):
    annotator = models.ForeignKey(to=FinprintUser)
    video = models.ForeignKey(to=Video)
    assigned_by = models.ForeignKey(to=FinprintUser, related_name='assigned_by')
    status = models.ForeignKey(to=AnnotationState, default=1)
    progress = models.IntegerField(default=0)

    def set(self):
        return self.video.set

    def update_progress(self, seconds):
        if seconds > self.progress:
            self.progress = seconds
            self.save()
        return self.progress

    @classmethod
    def get_active(cls):
        return cls.objects.filter(status_id__in=[1, 2])

    @classmethod
    def get_active_for_annotator(cls, annotator):
        return cls.get_active().filter(annotator=annotator)

    def to_json(self):
        return {'id': self.id,
                'set_code': str(self.set()),
                'file': str(self.video.file),
                'assigned_to': {'id': self.annotator.id, 'user': str(self.annotator)},
                'progress': self.progress}

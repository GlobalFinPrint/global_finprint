from django.db import models, connection
from global_finprint.core.models import AuditableModel, FinprintUser


# todo:  pull video file names into ranked list (for l & r, etc.)
class Video(AuditableModel):
    file = models.CharField(max_length=100, null=True, blank=True)
    source_folder = models.CharField(max_length=100, null=True, blank=True)

    def annotators_assigned(self):
        return list(a.annotator for a in self.assignment_set.all())

    def length(self):
        try:
            progress_list = self.assignment_set.exclude(status_id__in=[1, 2]).values_list('progress', flat=True)
            return max(p for p in progress_list if p > 0)
        except ValueError:
            try:
                sql = '''select max(e.event_time) from annotation_event e
                join annotation_observation o on (e.observation_id = o.id)
                join annotation_assignment a on (o.assignment_id = a.id)
                where a.video_id = %s'''
                with connection.cursor() as cursor:
                    cursor.execute(sql, [self.id])
                    return cursor.fetchone()[0]
            except:  # TODO be more specific here
                return None

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
        return cls.objects.filter(status_id__in=[1, 2, 3])

    @classmethod
    def get_active_for_annotator(cls, annotator):
        return cls.objects.filter(annotator=annotator, status_id__in=[1, 2])

    def to_json(self):
        last_activity = self.last_activity()
        return {'id': self.id,
                'set_code': str(self.set()),
                'file': str(self.video.file),
                'assigned_to': {'id': self.annotator.id, 'user': str(self.annotator)},
                'progress': self.progress,
                'status': {'id': self.status_id, 'name': self.status.name},
                'assigned_at': self.create_datetime.strftime('%b %d, %Y %I:%m %p'),
                'last_activity': last_activity.strftime('%b %d, %Y %I:%m %p') if last_activity else 'None'}

    def last_activity(self):
        sql = '''
        SELECT max(greatest(e.last_modified_datetime, o.last_modified_datetime))
        FROM annotation_observation o
        JOIN annotation_event e ON (e.observation_id = o.id)
        WHERE o.assignment_id = %s
        '''
        with connection.cursor() as cursor:
            cursor.execute(sql, [self.id])
            return cursor.fetchone()[0]

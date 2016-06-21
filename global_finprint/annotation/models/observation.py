from django.db import models
from django.contrib.gis.db import models as geomodels
from global_finprint.core.models import AuditableModel, FinprintUser
from django.conf import settings
from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
from .video import Assignment
from .animal import Animal, ANIMAL_SEX_CHOICES, ANIMAL_STAGE_CHOICES
from .annotation import Attribute
from ...core.version import VersionInfo


OBSERVATION_TYPE_CHOICES = {
    ('I', 'Of interest'),
    ('A', 'Animal'),
}


class Observation(AuditableModel):
    assignment = models.ForeignKey(Assignment)
    type = models.CharField(max_length=1, choices=OBSERVATION_TYPE_CHOICES, default='I')
    # duration could be redundant ... at best it's an optimization:
    duration = models.PositiveIntegerField(null=True, blank=True)
    comment = models.TextField(null=True)
    created_by = models.ForeignKey(to=FinprintUser, related_name='observations_created', null=True)
    updated_by = models.ForeignKey(to=FinprintUser, related_name='observations_updated', null=True)

    @staticmethod
    def create(**kwargs):
        kwargs['type'] = kwargs.pop('type_choice', None)
        kwargs['created_by'] = kwargs['user'].finprintuser
        kwargs['updated_by'] = kwargs['user'].finprintuser

        animal_fields = {
            'animal_id': kwargs.pop('animal_id', None),
            'sex': kwargs.pop('sex_choice', None),
            'stage': kwargs.pop('stage_choice', None),
            'length': kwargs.pop('length', None),
            'user': kwargs['user']
        }
        animal_fields = dict((k, v) for k, v in animal_fields.items() if v is not None)

        evt_fields = {
            'event_time': kwargs.pop('event_time', None),
            'extent': kwargs.pop('extent', None),
            'note': kwargs.pop('note', None),
            'attribute': kwargs.pop('attribute', None),
            'user': kwargs['user']
        }

        obs = Observation(**kwargs)
        obs.save()

        evt_fields['observation'] = obs
        Event.create(**evt_fields)

        if kwargs.get('type') == 'A':
            animal_fields['observation'] = obs
            animal_obs = AnimalObservation(**animal_fields)
            animal_obs.save()

        return obs

    @staticmethod
    def valid_fields():
        return [
            'type_choice',
            'duration',
            'comment',
            'animal_id',
            'sex_choice',
            'stage_choice',
            'length',
            # event fields
            'event_time',
            'extent',
            'note',
            'attribute'
        ]

    @classmethod
    def get_for_api(cls, assignment):
        return list(ob.to_json() for ob in cls.objects.filter(assignment=assignment))

    def set(self):
        return self.assignment.video.set

    def to_json(self):
        json = {
            'id': self.id,
            'type': self.get_type_display(),
            'type_choice': self.type,
            'duration': self.duration,
            'comment': self.comment,
            'events': [e.to_json() for e in self.event_set.all()]
        }

        if self.type == 'A':
            animal = self.animalobservation
            json.update({
                'animal': str(animal.animal),
                'animal_id': animal.animal_id,
                'sex': animal.get_sex_display(),
                'sex_choice': animal.sex,
                'stage': animal.get_stage_display(),
                'stage_choice': animal.stage,
                'length': animal.length,
            })

        return json

    def initial_observation_time(self):
        return self.event_set.order_by('event_time').first().event_time

    def events_for_table(self):
        return self.event_set.order_by('event_time').all()

    def __str__(self):
        # todo:  update to first event?
        return u"{0}".format(self.type)


class AnimalObservation(AuditableModel):
    observation = models.OneToOneField(to=Observation)
    animal = models.ForeignKey(Animal)
    sex = models.CharField(max_length=1,
                           choices=ANIMAL_SEX_CHOICES, default='U')
    stage = models.CharField(max_length=2,
                             choices=ANIMAL_STAGE_CHOICES, default='U')
    length = models.IntegerField(null=True, help_text='centimeters')

    def behavior_display(self):
        return list()


class Event(AuditableModel):
    observation = models.ForeignKey(to=Observation)

    event_time = models.IntegerField(help_text='ms', default=0)
    extent = geomodels.PolygonField(null=True)
    attribute = models.ManyToManyField(to=Attribute)
    note = models.TextField(null=True)

    @classmethod
    def create(cls, **kwargs):
        att_ids = kwargs.pop('attribute', [])
        evt = cls(**kwargs)
        evt.save()
        attributes = [Attribute.objects.get(pk=att_id) for att_id in att_ids]
        for att in attributes:
            evt.attribute.add(att)
        return evt

    @staticmethod
    def valid_fields():
        # attributes are added separately via event.attribute.add()
        return [
            'observation',
            'event_time',
            'extent',
            'note'
        ]

    def to_json(self):
        return {
            'id': self.pk,
            'event_time': self.event_time,
            'extent': None if self.extent is None else str(self.extent),
            'note': self.note,
            'attributes': [a.to_json() for a in self.attribute.all()]
        }

    def filename(self):
        set = self.observation.set()
        server_env = VersionInfo.get_server_env()
        return '/{0}/{1}/{2}/{3}_{4}.png'.format(server_env,
                                                 set.trip.code,
                                                 set.code,
                                                 self.observation_id,
                                                 self.id)

    def image_url(self):
        try:
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            bucket = conn.get_bucket(settings.FRAME_CAPTURE_BUCKET)
            key = bucket.get_key(self.filename())
            return key.generate_url(expires_in=300, query_auth=False) if key else None
        except S3ResponseError:
            return None

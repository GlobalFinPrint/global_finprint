import logging
from datetime import datetime

from boto.exception import S3ResponseError
from boto.s3.connection import S3Connection
from django.conf import settings
from django.contrib.gis.db import models as geomodels
from django.contrib.postgres.fields import JSONField
from django.db import transaction, models

from global_finprint.core.models import AuditableModel, FinprintUser
from .animal import Animal, ANIMAL_SEX_CHOICES, ANIMAL_STAGE_CHOICES
from .annotation import Attribute, Project
from .video import Assignment
from ...core.templatetags.time_display import time_display
from ...core.version import VersionInfo

SCREEN_CAPTURE_URL = 'https://s3-us-west-2.amazonaws.com/finprint-annotator-screen-captures'

logger = logging.getLogger(__name__)

MAXN_MEASURABLE_ID = 2

OBSERVATION_TYPE_CHOICES = {
    ('I', 'Of interest'),
    ('A', 'Animal'),
}


# 1 = In progress, 2 = Completed, 3 = Deprecated
class MasterRecordState(models.Model):
    name = models.TextField()
    description = models.TextField()

    @property
    def is_finished(self):
        """
        boolean for whether the master record is in one of the states that is deemed 'finished'.
        finished is either "completed" or "deprecated"
        """
        return True if self.id in [2, 3] else False

    def __str__(self):
        return u'{0}'.format(self.name)

    class Meta:
        ordering = ['id']


class MasterRecord(AuditableModel):
    set = models.ForeignKey(to='bruv.Set')
    note = models.TextField()

    status = models.ForeignKey(to=MasterRecordState, null=False)

    project = models.ForeignKey(Project, default=1)

    class Meta:
        unique_together = (('set', 'project'),)

    @transaction.atomic
    def copy_observations(self, observation_ids):
        try:
            for old_master_observation in self.masterobservation_set.all():
                old_master_observation.delete()
            for observation in Observation.objects.filter(pk__in=observation_ids):
                MasterObservation.create_from_original(self, observation)
            return True, None
        except Exception as e:
            return False, str(e)

    def original_observations(self):
        return list(obs.original for obs in self.masterobservation_set.all())

    def to_json(self):
        return {
            'observation_ids': list(obs.id for obs in self.masterobservation_set.all()),
            'set_id': self.set.id,
            'project_id': self.project.id,
            'status': self.status.name,
            'note': self.note,
            'original_observation_ids': list(obs.id for obs in self.original_observations()),
        }


class AbstractObservation(AuditableModel):
    type = models.CharField(max_length=1, choices=OBSERVATION_TYPE_CHOICES, default='I')
    # duration could be redundant ... at best it's an optimization:
    duration = models.PositiveIntegerField(null=True, blank=True)
    comment = models.TextField(null=True)
    observation_time = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    def initial_observation_time(self):
        if self.observation_time is None:
            self.observation_time = self.initial_event().event_time
            self.save()
        return self.observation_time


class Observation(AbstractObservation):
    assignment = models.ForeignKey(Assignment)
    created_by = models.ForeignKey(to=FinprintUser, related_name='observations_created', null=True)
    updated_by = models.ForeignKey(to=FinprintUser, related_name='observations_updated', null=True)

    @staticmethod
    def create(**kwargs):
        # todo: need to check if these actually exist and throw a nice error rather than failing in db and returning a bad 500
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
            'measurables': kwargs.pop('measurables', None),
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
            'attribute',
            'measurables'
        ]

    @classmethod
    def get_for_api(cls, assignment):
        return list(ob.to_json() for ob in cls.objects.filter(assignment=assignment))

    def remove_relations(self):
        # remove events
        self.event_set.all().delete()
        # remove animal
        if hasattr(self, 'animalobservation'):
            self.animalobservation.delete()

    def set(self):
        return self.assignment.video.set

    def to_json(self, for_web=False):
        json = {
            'id': self.id,
            'type': self.get_type_display(),
            'type_choice': self.type,
            'duration': self.duration,
            'comment': self.comment,
            'create_datetime': self.create_datetime,
            'events': [e.to_json(for_web=for_web) for e in self.event_set.all()]
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
                'group': animal.animal.group.id,
                'group_name': str(animal.animal.group)
            })

        if for_web:
            json['time'] = self.initial_observation_time()
            json['pretty_time'] = time_display(self.initial_observation_time())
            json['initial_event'] = self.initial_event().to_json(for_web=True)
        return json

    def initial_event(self):
        return self.event_set.order_by('create_datetime').first()

    def event_set_for_table(self):
        initial_event = self.initial_event()
        return [initial_event] + list(self.event_set.exclude(id=initial_event.id).order_by('-event_time'))

    def __str__(self):
        # todo:  update to first event?
        return u"{0}".format(self.type)

    def annotator(self):
        return self.assignment.annotator

    def animal(self):
        return self.animalobservation.animal

    def needs_review(self):
        return any(e.needs_review() for e in self.event_set.all())


class MasterObservation(AbstractObservation):
    master_record = models.ForeignKey(to=MasterRecord)
    original = models.ForeignKey(to=Observation, null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(to=FinprintUser, related_name='master_observations_created', null=True)
    updated_by = models.ForeignKey(to=FinprintUser, related_name='master_observations_updated', null=True)

    @classmethod
    def create_from_original(cls, master_record, original_observation):
        master_observation = cls(
            type=original_observation.type,
            duration=original_observation.duration,
            comment=original_observation.comment,
            master_record=master_record,
            original=original_observation,
            created_by=original_observation.created_by,
            updated_by=original_observation.updated_by
        )
        master_observation.save()

        if original_observation.type == 'A':
            MasterAnimalObservation.create_from_original(master_observation, original_observation.animalobservation)

        for event in original_observation.event_set.all():
            MasterEvent.create_from_original(master_observation, event)

    def set(self):
        return self.master_record.set

    def initial_event(self):
        return self.masterevent_set.order_by('original_id').first()

    def event_set(self):
        return self.masterevent_set.order_by('event_time')

    def annotator(self):
        return self.original.annotator()

    def animal(self):
        return self.masteranimalobservation.animal

    def event_set_for_table(self):
        initial_event = self.initial_event()
        return [initial_event] + list(self.masterevent_set.exclude(id=initial_event.id).order_by('-event_time'))

    def needs_review(self):
        return any(e.needs_review() for e in self.event_set())


class AbstractAnimalObservation(AuditableModel):
    animal = models.ForeignKey(Animal)
    sex = models.CharField(max_length=1, choices=ANIMAL_SEX_CHOICES, default='U')
    stage = models.CharField(max_length=2, choices=ANIMAL_STAGE_CHOICES, default='U')
    length = models.IntegerField(null=True, help_text='centimeters')

    class Meta:
        abstract = True


class AnimalObservation(AbstractAnimalObservation):
    observation = models.OneToOneField(to=Observation)

    def behavior_display(self):
        return list()


class MasterAnimalObservation(AbstractAnimalObservation):
    master_observation = models.OneToOneField(to=MasterObservation)
    original = models.ForeignKey(to=AnimalObservation, null=True, blank=True, on_delete=models.SET_NULL)

    @classmethod
    def create_from_original(cls, master_observation, original_animal_observation):
        master_animal_observation = cls(
            animal=original_animal_observation.animal,
            sex=original_animal_observation.sex,
            stage=original_animal_observation.stage,
            length=original_animal_observation.length,
            master_observation=master_observation,
            original=original_animal_observation
        )
        master_animal_observation.save()


class AbstractEvent(AuditableModel):
    event_time = models.IntegerField(help_text='ms', default=0)
    extent = geomodels.PolygonField(null=True)
    attribute = models.ManyToManyField(to=Attribute)
    note = models.TextField(null=True)

    class Meta:
        abstract = True

    # TODO: do we need to check for every key? maybe just use filename and a base_url
    def image_url(self, verify=False):
        if self.extent is None:
            logger.debug('{}'.format('No image extent: '))
            return None

        if verify is False:
            return '{}{}'.format(SCREEN_CAPTURE_URL, self.filename())

        try:
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            bucket = conn.get_bucket(settings.FRAME_CAPTURE_BUCKET)
            key = bucket.get_key(self.filename())
            return key.generate_url(expires_in=300, query_auth=False) if key else None
        except S3ResponseError as e:
            logger.warning('{}{}'.format('Unable to build image url: ', e.message))
            return None

            # TODO: do we need to check for every key? maybe just use filename and a base_url

    def clip_url(self, verify=False):
        if self.extent is None:
            logger.debug('{}'.format('No clip extent: '))
            return None

        self.clip_filename = None

        if self.filename() is not None:
            _splits = self.filename().split("/")
            _len = len(_splits)
            clip_filename = _splits[_len - 1].split(".")[0] + ".mp4"
            self.clip_filename = self.filename().strip(_splits[_len - 1]) + clip_filename
            logger.info('{}{}'.format('8 sec clip file name: ', self.clip_filename))

        if verify is False:
            return '{}{}'.format(SCREEN_CAPTURE_URL, self.clip_filename)

        try:
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            bucket = conn.get_bucket(settings.FRAME_CAPTURE_BUCKET)
            key = bucket.get_key(self.clip_filename)
            return key.generate_url(expires_in=300, query_auth=False) if key else None
        except S3ResponseError as e:
            logger.warning('{}{}'.format('Unable to build clip url: ', e.message))
            return None

    def extent_to_css(self):
        if self.extent is None:
            logger.debug('{}'.format('No image extent: '))
            return None

        try:
            x = self.extent.boundary.x
            y = self.extent.boundary.y
            css = 'width: {0}%; height: {1}%; left: {2}%; top: {3}%;'.format(
                int(abs(max(x) - min(x)) * 100),
                int(abs(max(y) - min(y)) * 100),
                int(min(x) * 100),
                int(min(y) * 100)
            )
            return css
        except AttributeError as e:  # handle bad extents
            logger.warning('{}{}'.format('Bad image extent: ', e.message))
            return None

    def needs_review(self):
        return any(a.needs_review for a in self.attribute.all())


class Measurable(models.Model):
    name = models.TextField()
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return u"{0}".format(self.name)


class Event(AbstractEvent):
    measurables = models.ManyToManyField(Measurable, through='EventMeasurable')
    observation = models.ForeignKey(to=Observation)
    raw_import_json = JSONField(null=True)

    def active_measurables(self):
        return self.eventmeasurable_set.filter(measurable__active=True)

    @classmethod
    def create(cls, **kwargs):
        # todo:  this implementation assumes we are only get lists of attribute_ids and measurable_values
        # ... rather than list of attribute and measurable objects
        # ... hence we make the [weak] assumption that the measurables are all MaxN and use the MAXN_MEASURABLE_ID constant
        att_ids = kwargs.pop('attribute', [])
        measurable_values = kwargs.pop('measurables', [])
        evt = cls(**kwargs)
        evt.save()
        attributes = [Attribute.objects.get(pk=att_id) for att_id in att_ids]
        for att in attributes:
            evt.attribute.add(att)
        for measurable_value in measurable_values:
            EventMeasurable(
                value=measurable_value,
                event=evt,
                measurable=Measurable(pk=MAXN_MEASURABLE_ID)
            ).save()
        return evt

    @staticmethod
    def valid_fields():
        # attributes are added separately via event.attribute.add()
        return [
            'observation',
            'event_time',
            'extent',
            'note',
            'raw_import_json',
            'measurables',
        ]

    def to_json(self, for_web=False):
        json = {
            'id': self.pk,
            'event_time': self.event_time,
            'extent': None if self.extent is None else str(self.extent),
            'note': self.note,
            'attribute': [a.to_json(children=not for_web) for a in self.attribute.all()],
            'measurables': [m.to_json() for m in self.active_measurables()],
            'create_datetime': datetime.strftime(self.create_datetime, '%Y-%m-%d %H:%M:%S')
        }

        if for_web:
            json['extent_css'] = self.extent_to_css()
            json['image_url'] = self.image_url(verify=False)
            json['clip_url'] = self.clip_url(verify=False)
            json['attribute_names'] = list(a.name for a in self.attribute.all())
            json['measurables'] = list(str(m) for m in self.active_measurables())

        return json

    def filename(self):
        set = self.observation.set()
        server_env = VersionInfo.get_server_env()
        return '/{0}/{1}/{2}/{3}_{4}.png'.format(server_env,
                                                 set.trip.code,
                                                 set.code,
                                                 self.observation_id,
                                                 self.id)


class MasterEvent(AbstractEvent):
    master_observation = models.ForeignKey(to=MasterObservation)
    measurables = models.ManyToManyField(Measurable, through='MasterEventMeasurable')
    original = models.ForeignKey(to=Event, null=True, blank=True, on_delete=models.SET_NULL)

    @classmethod
    def create_from_original(cls, master_observation, original_event):
        master_event = cls(
            event_time=original_event.event_time,
            extent=original_event.extent,
            note=original_event.note,
            master_observation=master_observation,
            original=original_event
        )
        master_event.save()
        for attribute in original_event.attribute.all():
            master_event.attribute.add(attribute)
        for measurable in original_event.active_measurables():
            master_measurable = MasterEventMeasurable(
                master_event=master_event,
                measurable=measurable.measurable,
                value=measurable.value
            )
            master_measurable.save()

    def filename(self):
        return self.original.filename()

    def active_measurables(self):
        return self.mastereventmeasurable_set.filter(measurable__active=True)


class EventMeasurable(models.Model):
    event = models.ForeignKey(Event)
    measurable = models.ForeignKey(Measurable)
    value = models.TextField()

    def to_json(self):
        json = {
            'id': self.pk,
            'measurable_id': self.measurable.id,
            'measurable_name': self.measurable.name,
            'value': self.value
        }
        return json

    def __str__(self):
        return u"{}: {}".format(self.measurable, self.value)

    class Meta:
        unique_together = ('event', 'measurable')


class MasterEventMeasurable(models.Model):
    master_event = models.ForeignKey(MasterEvent)
    measurable = models.ForeignKey(Measurable)
    value = models.TextField()

    def __str__(self):
        return u"{}: {}".format(self.measurable, self.value)

    class Meta:
        unique_together = ('master_event', 'measurable')

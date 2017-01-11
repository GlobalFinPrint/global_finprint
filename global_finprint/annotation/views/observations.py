from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from global_finprint.annotation.models.observation import \
    Observation, Event, Animal, Attribute, MasterEvent
from global_finprint.bruv.models import Set, Trip
from global_finprint.core.mixins import UserAllowedMixin


# deprecated:
@login_required
def observation_detail(request, pk):
    observation = Observation.objects.get(pk=pk)
    data = {
            'id': str(observation.id),
            # 'initial_observation_time': observation.initial_observation_time.isoformat(),
            'animal': str(observation.animal),
            'sex': observation.sex,
            'stage': observation.stage,
            'length': str(observation.length),
            'behavior': observation.behavior,
            'set': str(observation.set),
            'observer': str(observation.observer),
            }
    return JsonResponse(data)


def observation_post(request):
    pass


class ObservationListView(UserAllowedMixin, ListView):
    model = Observation
    context_object_name = 'observations'
    template_name = 'pages/observations/observation_list.html'

    def get_queryset(self):
        selected_related = [
            'animalobservation__animal',
            'assignment__annotator__user',
            'assignment__annotator__affiliation',
            'assignment__video__set__trip',
        ]
        return sorted(get_object_or_404(Set, pk=self.kwargs['set_pk']).observations()
                      .select_related(*selected_related)
                      .prefetch_related('event_set', 'event_set__attribute'),
                      key=lambda o: o.initial_observation_time(), reverse=True)

    def get_context_data(self, **kwargs):
        context = super(ObservationListView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(context['observations'], 50)
        try:
            context['observations'] = paginator.page(page)
        except PageNotAnInteger:
            context['observations'] = paginator.page(1)
        except EmptyPage:
            context['observations'] = paginator.page(paginator.num_pages)
        context['trip_pk'] = self.kwargs['trip_pk']
        context['set_pk'] = self.kwargs['set_pk']
        context['trip_name'] = str(Trip.objects.get(pk=self.kwargs['trip_pk']))
        context['set_name'] = str(Set.objects.get(pk=self.kwargs['set_pk']))
        context['for'] = ' for {0}'.format(context['set_name'])
        return context


# TODO DRY this up
class MasterObservationEditData(UserAllowedMixin, View):
    def get(self, request, evt_id, **kwargs):
        event = get_object_or_404(MasterEvent, pk=evt_id)
        project = event.master_observation.master_record.project
        animals = Animal.objects.filter(project=project).select_related('group')
        tags = project.attribute_set.all()
        return JsonResponse({
            'animals': list({'id': a.id, 'name': str(a)} for a in animals),
            'tags': list({'id': t.id, 'name': str(t)} for t in tags),
            'selected_animal': event.master_observation.animal().id if event.master_observation.type == 'A' else None,
            'obs_note': event.master_observation.comment,
            'duration': event.master_observation.duration,
            'event_note': event.note,
            'selected_tags': list(a.id for a in event.attribute.all())
        })


# TODO DRY this up
class MasterObservationSaveData(UserAllowedMixin, View):
    def post(self, request, evt_id, **kwargs):
        event = get_object_or_404(MasterEvent, pk=evt_id)
        observation = event.master_observation

        is_obs = request.POST.get('is_obs', 'false')
        animal_id = request.POST.get('animal_id', None)
        obs_note = request.POST.get('obs_note', None)
        duration = request.POST.get('duration', None)
        event_note = request.POST.get('event_note', None)
        tags = list(int(t) for t in request.POST.getlist('tags[]', []))

        with transaction.atomic():
            if is_obs != 'false':
                if observation.type == 'A':
                    animal = get_object_or_404(Animal, pk=animal_id)
                    observation.masteranimalobservation.animal = animal
                    observation.masteranimalobservation.save()
                observation.comment = obs_note if obs_note is not '' else None
                try:
                    observation.duration = int(duration)
                except ValueError:
                    observation.duration = None
                observation.save()
            event.note = event_note if event_note is not '' else None
            event.attribute.clear()
            for att in Attribute.objects.filter(id__in=tags).all():
                event.attribute.add(att)
            event.save()

        return JsonResponse({
            'animal': str(observation.animal()) if event.master_observation.type == 'A' else '<i>N/A</i>',
            'obs_note': observation.comment if observation.comment is not None else '<i>None</i>',
            'duration': observation.duration if observation.duration is not None else '<i>None</i>',
            'event_note': event.note if event.note is not None else '<i>None</i>',
            'attributes': ', '.join(map(str, event.attribute.all())),
        })


class ObservationEditData(UserAllowedMixin, View):
    def get(self, request, evt_id, **kwargs):
        event = get_object_or_404(Event, pk=evt_id)
        project = event.observation.assignment.project
        animals = Animal.objects.filter(project=project).select_related('group')
        tags = project.attribute_set.all()
        return JsonResponse({
            'animals': list({'id': a.id, 'name': str(a)} for a in animals),
            'tags': list({'id': t.id, 'name': str(t)} for t in tags),
            'selected_animal': event.observation.animal().id if event.observation.type == 'A' else None,
            'obs_note': event.observation.comment,
            'duration': event.observation.duration,
            'event_note': event.note,
            'selected_tags': list(a.id for a in event.attribute.all())
        })


class ObservationSaveData(UserAllowedMixin, View):
    def post(self, request, evt_id, **kwargs):
        event = get_object_or_404(Event, pk=evt_id)
        observation = event.observation

        is_obs = request.POST.get('is_obs', 'false')
        animal_id = request.POST.get('animal_id', None)
        obs_note = request.POST.get('obs_note', None)
        duration = request.POST.get('duration', None)
        event_note = request.POST.get('event_note', None)
        tags = list(int(t) for t in request.POST.getlist('tags[]', []))

        with transaction.atomic():
            if is_obs != 'false':
                if observation.type == 'A':
                    animal = get_object_or_404(Animal, pk=animal_id)
                    observation.animalobservation.animal = animal
                    observation.animalobservation.save()
                observation.comment = obs_note if obs_note is not '' else None
                try:
                    observation.duration = int(duration)
                except ValueError:
                    observation.duration = None
                observation.save()
            event.note = event_note if event_note is not '' else None
            event.attribute.clear()
            for att in Attribute.objects.filter(id__in=tags).all():
                event.attribute.add(att)
            event.save()

        return JsonResponse({
            'animal': str(observation.animal()) if event.observation.type == 'A' else '<i>N/A</i>',
            'obs_note': observation.comment if observation.comment is not None else '<i>None</i>',
            'duration': observation.duration if observation.duration is not None else '<i>None</i>',
            'event_note': event.note if event.note is not None else '<i>None</i>',
            'attributes': ', '.join(map(str, event.attribute.all())),
        })

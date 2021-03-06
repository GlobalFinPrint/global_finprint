import json

from django.http.response import HttpResponse

from global_finprint.habitat.models import Region, Site, Location

from ..models.animal import Animal, AnimalGroup
from ..models.video import Video, Assignment


# deprecated:
def site_animal_list(request, site_id, *args, **kwargs):
    """
    :param request:
    :param site_id:  the site_id for the video to annotated
    :return:
    animal lists based on region that the site is in:
        lists:
        - sharks
        - rays
        - other targets
        - groupers, jacks, other fish of interest
        - all
    """
    # todo: sanity check if 'limit' can be cast to int
    limit = (int(request.REQUEST['limit']) if 'limit' in request.REQUEST else 5)
    animals = Animal.objects.filter(
        regions=Region.objects.filter(pk=Location.objects.filter(pk=Site.objects.filter(pk=site_id))))
    animal_lists = {
        'all': [],
    }
    for animal_group in AnimalGroup.objects.all():
        animal_lists[animal_group.name] = []
    for animal in animals:
        animal_dict = {
            'rank': animal.rank,
            'group': animal.group.name,
            'common_name': animal.common_name,
            'family': animal.family,
            'genus': animal.genus,
            'species': animal.species,
            'fishbase_key': animal.fishbase_key,
            'fishbase_url': 'http://www.fishbase.org/summary/{0}'.format(animal.fishbase_key)
            if animal.fishbase_key else None,
            'sealifebase_key': animal.sealifebase_key,
            'sealifebase_url': 'http://www.sealifebase.org/summary/{0}'.format(animal.sealifebase_key)
            if animal.sealifebase_key else None,
            'caab_code': animal.caab_code,
        }
        animal_lists['all'].append(animal_dict)
        if animal.rank <= limit:
            animal_lists[animal.group.name].append(animal_dict)

    return HttpResponse(json.dumps(animal_lists), content_type='application/json')


# deprecated:
def annotator_video_list(request, annotator_id):
    videos = Video.objects.filter(pk=Assignment(annotator=annotator_id))

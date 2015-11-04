import json
from django.http.response import HttpResponse

from ..models import Animal, Video, VideoAnnotator


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
    animals = Animal.objects.all()
    animal_lists = {
        'sharks': [],
        'rays': [],
        'other_targets': [],
        'groupers_jacks': [],
        'all': [],
    }
    for animal in animals:
        animal_dict = {
            'rank': animal.rank,
            'group': animal.group,
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
        }
        animal_lists['all'].append(animal_dict)
        # todo:  just filter all list subsets and order by rank!
        if animal.group == 'S' and animal.rank <= limit:
            animal_lists['sharks'].append(animal_dict)
        elif animal.group == 'R' and animal.rank <= limit:
            animal_lists['rays'].append(animal_dict)
        elif animal.group == 'T' and animal.rank <= limit:
            animal_lists['other_targets'].append(animal_dict)
        elif animal.group == 'G' and animal.rank <= limit:
            animal_lists['groupers_jacks'].append(animal_dict)
    return HttpResponse(json.dumps(animal_lists), content_type='application/json')


def annotator_video_list(request, annotator_id):
    videos = Video.objects.filter(pk=VideoAnnotator(annotator=annotator_id))

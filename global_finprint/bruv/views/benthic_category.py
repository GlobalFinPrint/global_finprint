from django.views.generic import View
from django.http import JsonResponse
from global_finprint.core.mixins import UserAllowedMixin
from global_finprint.bruv.models import BenthicCategory


class BenthicCategoryView(UserAllowedMixin, View):
    """
    Endpoint to power benthic category widget
    """
    def get(self, request):
        if 'parent_id' in request.GET:
            substrates = BenthicCategory.objects.filter(parent_id=request.GET.get('parent_id'))
        else:
            substrates = BenthicCategory.objects.all()
        return JsonResponse({'substrates': [{'id': s.id, 'name': (s.get_level() * '-' + ' ') + s.name}
                                            for s in substrates]})

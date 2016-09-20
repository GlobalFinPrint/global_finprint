from django.views.generic import View
from django.http import JsonResponse
from global_finprint.core.mixins import UserAllowedMixin
from global_finprint.bruv.models import Substrate


class HabitatSubstrate(UserAllowedMixin, View):
    def get(self, request):
        if 'parent_id' in request.GET:
            substrates = Substrate.objects.filter(parent_id=request.GET.get('parent_id'))
        else:
            substrates = Substrate.objects.all()
        return JsonResponse({'substrates': [{'id': s.id, 'name': s.name} for s in substrates]})

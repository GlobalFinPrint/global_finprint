from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import HttpResponse

from .models import Reef


# depracated:
@login_required
def reef_detail_geojson(request, reef_id):
    feature = serialize('geojson',
                        Reef.objects.filter(id=reef_id),
                        fields='name, boundary,'
                        )
    return HttpResponse(feature, content_type='application/json')

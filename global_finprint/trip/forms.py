from django.forms import ModelForm
from global_finprint.trip import models


class TripForm(ModelForm):
    class Meta:
        fields = {'name', 'location', 'start_datetime', 'end_datetime', 'team', 'boat', 'type'}
        model = models.Trip


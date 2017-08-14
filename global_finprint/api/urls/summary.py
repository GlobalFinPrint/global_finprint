from django.conf.urls import url

from ...report.views import HabitatSummaryView, ObservationSummaryView, SetSummaryView

urlpatterns = [

    url(r"habitat/$", HabitatSummaryView.as_view(), name="habitats"),
    url(r"observation/(?P<region>[\w ]+)$", ObservationSummaryView.as_view(), name="observation_summary"),
    url(r"set/(?P<region>[\w ]+)$", SetSummaryView.as_view(), name="set_summary"),

]

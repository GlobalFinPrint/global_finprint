from django.conf.urls import url, include
from .views import CustomReportListView, CustomReportView, \
    CustomReportFileView, LeaderboardView, StatusMapView, \
    HabitatSummaryView, ObservationSummaryView, SetSummaryView


urlpatterns = [
    url(r'builder/', include('report_builder.urls'), name="report_builder"),
    url(r"leaderboard/$", LeaderboardView.as_view(), name="report_leaderboard"),

    url(r"status/map/$", StatusMapView.as_view(), name="status_map"),

    url(r"custom/(?P<report>\w+)$", CustomReportView.as_view(), name="report_custom"),
    # todo:  generify the format from only .csv?
    url(r"custom/(?P<report>\w+).(?P<format>\w+)$", CustomReportFileView.as_view(), name="report_custom_csv"),

    url(r"habitat/$", HabitatSummaryView.as_view(), name="habitats"),
    url(r"observation/summary/(?P<region>[\w ]+)$", ObservationSummaryView.as_view(), name="observation_summary"),
    url(r"set/summary/(?P<region>[\w ]+)$", SetSummaryView.as_view(), name="set_summary"),

    url(r"$", CustomReportListView.as_view(), name="report_home"),
]

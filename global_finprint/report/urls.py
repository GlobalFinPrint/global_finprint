from django.conf.urls import url, include
from .views import StandardReportListView, StandardReportView, \
    StandardReportFileView, LeaderboardView, StatusMapView

urlpatterns = [
    url(r'builder/', include('report_builder.urls'), name="report_builder"),
    url(r"leaderboard/$", LeaderboardView.as_view(), name="report_leaderboard"),

    url(r"status/map/$", StatusMapView.as_view(), name="status_map"),

    url(r"standard/(?P<report>\w+)$", StandardReportView.as_view(), name="report_standard"),
    url(r"standard/(?P<report>\w+)/(?P<limit>[0-9]+)$", StandardReportView.as_view(), name="report_standard"),
    # todo:  generify the format from only .csv?
    url(r"standard/(?P<report>\w+).(?P<format>\w+)$", StandardReportFileView.as_view(), name="report_standard_csv"),

    url(r"$", StandardReportListView.as_view(), name="report_home"),
]

from django.conf.urls import url, include
from .views import CustomReportListView, StandardReportView, \
    StandardReportFileView, LeaderboardView, StatusMapView

urlpatterns = [
    url(r'builder/', include('report_builder.urls'), name="report_builder"),
    url(r"leaderboard/$", LeaderboardView.as_view(), name="report_leaderboard"),

    url(r"status/map/$", StatusMapView.as_view(), name="status_map"),

    url(r"standard/(?P<report>\w+)$", StandardReportView.as_view(), name="report_standard"),
    # todo:  generify the format from only .csv?
    url(r"standard/(?P<report>\w+).(?P<format>\w+)$", StandardReportFileView.as_view(), name="report_standard_csv"),

    url(r"$", CustomReportListView.as_view(), name="report_home"),
]

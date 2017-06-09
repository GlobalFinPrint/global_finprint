from django.conf.urls import url, include
from .views import CustomReportListView, CustomReportView, CustomReportFileView, StatusMapView


urlpatterns = [
    url(r'builder/', include('report_builder.urls'), name="report_builder"),
    url(r"leaderboard/$", CustomReportListView.as_view(), name="report_leaderboard"),

    url(r"status/map/$", StatusMapView.as_view(), name="status_map"),

    url(r"custom/(?P<report>\w+)$", CustomReportView.as_view(), name="report_custom"),
    # todo:  generify the format from only .csv?
    url(r"custom/(?P<report>\w+).(?P<format>\w+)$", CustomReportFileView.as_view(), name="report_custom_csv"),
    url(r"$", CustomReportListView.as_view(), name="report_home"),

]

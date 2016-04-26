from django.conf.urls import url
from .views import CustomReportListView, CustomReportView, CustomReportFileView


urlpatterns = [
    url(r"custom/(?P<report>\w+)$", CustomReportView.as_view(), name="report_custom"),
    # todo:  generify the format from only .csv?
    url(r"custom/(?P<report>\w+).(?P<format>\w+)$", CustomReportFileView.as_view(), name="report_custom_csv"),
    url(r"$", CustomReportListView.as_view(), name="report_home"),
]

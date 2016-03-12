from django.conf.urls import url
from .views import CustomReportListView, CustomReportView


urlpatterns = [
    url(r"custom/(?P<report>\w+)$", CustomReportView.as_view(), name="report_custom"),
    url(r"$", CustomReportListView.as_view(), name="report_home"),
]

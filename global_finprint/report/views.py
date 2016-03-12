from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import Report
from ..core.mixins import UserAllowedMixin


class CustomReportListView(UserAllowedMixin, View):
    template = 'pages/reports/custom_list.html'

    def get(self, request):
        context = RequestContext(request, {'reports': Report.view_list()})
        return render_to_response(self.template, context=context)


class CustomReportView(UserAllowedMixin, View):
    template = 'pages/reports/custom_report.html'

    def get(self, request, report):
        report = Report(report)
        results = report.results()
        context = RequestContext(request, {
            'report': report,
            'headers': results[0],
            'rows': results[1:]
        })
        return render_to_response(self.template, context=context)

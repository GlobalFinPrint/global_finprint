import csv

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import Report, Planned_Site_Status
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


class CustomReportFileView(UserAllowedMixin, View):
    # todo:  always csv right now ... handle other formats?
    def get(self, request, report, format):
        report = Report(report)
        results = report.results()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(report)

        writer = csv.writer(response)
        writer.writerows(results)

        return response


class StatusMapView(UserAllowedMixin, View):
    template = 'pages/reports/status_report_map.html'

    def get(self, request):
        return render_to_response(self.template)

@login_required
def planned_site_geojson(request):
    feature = serialize('geojson',
                        Planned_Site_Status.objects.all(),
                        fields='eez_boundary, status'
                        )
    return HttpResponse(feature, content_type='application/json')

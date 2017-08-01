import csv

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.serializers import serialize
from django.http import HttpResponse, HttpRequest

from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.shortcuts import render
from django.db.models import Count

from .models import Report, PlannedSiteStatus, HabitatSummary, ObservationSummary, SetSummary
from ..annotation.models.video import Assignment
from ..core.mixins import UserAllowedMixin


class CustomReportListView(UserAllowedMixin, View):
    """
    List for custom reports found at /reports/
    """
    template = 'pages/reports/custom_list.html'

    def get(self, request):
        context = {'reports': Report.view_list()}
        return render(request, self.template, context=context)


class CustomReportView(UserAllowedMixin, View):
    """
    Individual report view found at /reports/custom/<report_name>
    """
    template = 'pages/reports/custom_report.html'

    def get(self, request, report):
        report = Report(report)
        results = report.results()
        context = {
            'report': report,
            'headers': results[0],
            'rows': results[1:]
        }
        return render(request, self.template, context=context)


class CustomReportFileView(UserAllowedMixin, View):
    """
    Download report as CSV view
    """
    # todo:  always csv right now ... handle other formats?
    def get(self, request, report, format):
        report = Report(report)
        results = report.results()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(report)

        writer = csv.writer(response)
        writer.writerows(results)

        return response


class LeaderboardView(View):
    """
    Top annotators
    """
    template = 'pages/reports/leaderboard.html'

    def get(self, request):
        overall_leaders = Assignment.objects.values(
            'annotator__user__last_name', 'annotator__user__first_name', 'annotator__affiliation__name').exclude(
            annotator__affiliation_id__in=(0, 1, 7)).filter(status_id__in=(3, 4)).annotate(
            num_assignments=Count('id')).order_by('-num_assignments')[:25]
        monthly_leaders = Assignment.objects.values(
            'annotator__user__last_name', 'annotator__user__first_name',
            'annotator__affiliation__name').exclude(
            annotator__affiliation_id__in=(0, 1, 7)).filter(status_id__in=(3, 4)).annotate(
            num_assignments=Count('id')).order_by('-last_modified_year_month', '-num_assignments')[:25]
        context = {
            'overall_leaders': overall_leaders,
            'monthly_leaders': monthly_leaders
        }
        return render(request, self.template, context=context)


class HabitatSummaryView(View):
    def get(self, request):
        return JsonResponse({'habitats': HabitatSummary.get_for_api()})


class ObservationSummaryView(View):
    def get(self, request, region):
        return JsonResponse({'region': region, 'observations': ObservationSummary.get_for_api(region)})


class SetSummaryView(View):
    def get(self, request, region):
        return JsonResponse({'region': region, 'sets': SetSummary.get_for_api(region)})


# todo: not currently used ... intended for status mapping.
class StatusMapView(UserAllowedMixin, View):
    """
    Report for status map found at /reports/status/map/
    """
    template = 'pages/reports/status_report_map.html'

    def get(self, request):
        return render(request, self.template)

def report(request):
    """ Renders the custom reports page"""
    assert isinstance(request, HttpRequest)
    settings.REPORT_BUILDER_INCLUDE = ['report.models.Report']
    return render(
        request,
        'report_builder/report.html',
        {

        }
    )

@login_required
def planned_site_geojson(request):
    """
    return geojson for planned sites
    :param request:
    :return:
    """
    feature = serialize('geojson',
                        PlannedSiteStatus.objects.all(),
                        fields='eez_boundary, status'
                        )
    return HttpResponse(feature, content_type='application/json')

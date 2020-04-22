import csv
import logging

from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize

from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.shortcuts import render
from django.db.models import Count, Sum, ExpressionWrapper, DecimalField

from .models import Report, PlannedSiteStatus, \
    HabitatSummary, ObservationSummary, SetSummary, \
    MonthlyLeaderboard
from ..annotation.models.video import Assignment
from ..core.mixins import UserAllowedMixin


class StandardReportListView(UserAllowedMixin, View):
    """
    List for custom reports found at /reports/
    """
    template = 'pages/reports/standard_list.html'
    DEFAULT_REPORT_LIMIT = 25

    def get(self, request):
        context = {
            'reports': Report.view_list(),
            'limit': self.DEFAULT_REPORT_LIMIT
        }
        return render(request, self.template, context=context)


class StandardReportView(UserAllowedMixin, View):
    """
    Individual report view found at /reports/custom/<report_name>
    """
    template = 'pages/reports/standard_report.html'

    def get(self, request, report, limit=None):
        logging.basicConfig(filename="test.log", level=logging.DEBUG)
        logging.error('Testing')
        logging.error('%s', report)
        report = Report(report)
        if not limit:
            limit = 'all'
        results = report.results(limit)
        context = {
            'report': report,
            'headers': results[0],
            'rows': results[1:],
            'limit': limit,
        }
        return render(request, self.template, context=context)


class StandardReportFileView(UserAllowedMixin, View):
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
        overall_leaders_hour = Assignment.objects.values(
            'annotator__user__last_name', 'annotator__user__first_name', 'annotator__affiliation__name').exclude(
            annotator__affiliation_id__in=(0, 1, 7)).filter(status_id__in=(3, 4)).annotate(
            hours=ExpressionWrapper(Sum('progress') / 1000 / 60 / 60,
                                    output_field=DecimalField(max_digits=12, decimal_places=2))).order_by('-hours')[:25]
        monthly_count_leaders = MonthlyLeaderboard.objects.all().order_by('-month', 'affiliation_name', 'affiliation_count_rank')
        monthly_hour_leaders = MonthlyLeaderboard.objects.all().order_by('-month', 'affiliation_name', 'affiliation_hour_rank')
        context = {
            'overall_leaders': overall_leaders,
            'overall_leaders_by_hour': overall_leaders_hour,
            'monthly_count_leaders': monthly_count_leaders,
            'monthly_hour_leaders': monthly_hour_leaders,
        }
        return render(request, self.template, context=context)


class HabitatSummaryView(View):
    def get(self, request):
        return JsonResponse({'habitats': HabitatSummary.get_for_api()})


class ObservationSummaryView(View):
    def get(self, request, region=None):
        return JsonResponse({'region': region, 'observations': ObservationSummary.get_for_api(region)})


class SetSummaryView(View):
    def get(self, request, region=None):
        return JsonResponse({'region': region, 'sets': SetSummary.get_for_api(region)})


# todo: not currently used ... intended for status mapping.
class StatusMapView(UserAllowedMixin, View):
    """
    Report for status map found at /reports/status/map/
    """
    template = 'pages/reports/status_report_map.html'

    def get(self, request):
        return render(request, self.template)


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

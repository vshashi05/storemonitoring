import csv
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import StatusUpdate, Store

class TriggerReportView(View):
    def get(self, request):
        report_data = [
            {
                'store_id': '',
                'uptime_last_hour': 0,
                'uptime_last_day': 0,
                'update_last_week': 0,
                'downtime_last_hour': 0,
                'downtime_last_day': 0,
                'downtime_last_week': 0,
            },
            {
                'store_id': 'ABC123',
                'uptime_last_hour': 98,
                'uptime_last_day': 95,
                'update_last_week': 100,
                'downtime_last_hour': 2,
                'downtime_last_day': 5,
                'downtime_last_week': 10,
            }
        ]
        if not report_data:
            return HttpResponse('No data available for the report.')

        fieldnames = ['store_id', 'uptime_last_hour', 'uptime_last_day', 'update_last_week', 'downtime_last_hour',
                      'downtime_last_day', 'downtime_last_week']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_data)

        return response


class GetReportView(View):
    def get(self, request):
        report_id = request.GET.get('report_id')
        if report_id is None:
            return JsonResponse({'error': 'Report ID is missing.'}, status=400)

        report_data = self.fetch_report(report_id)
        if report_data is None:
            return JsonResponse({'error': 'Report not found'}, status=404)

        return JsonResponse(report_data)

    def fetch_report(self, report_id):
        if report_id == '1':
            return {
                'store_id': 'ABC123',
                'uptime_last_hour': 98,
                'uptime_last_day': 95,
                'update_last_week': 100,
                'downtime_last_hour': 2,
                'downtime_last_day': 5,
                'downtime_last_week': 10,
            }
        else:
            return None

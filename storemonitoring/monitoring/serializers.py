from django.core.serializers import serialize
import json

class ReportSerializer:
    def __init__(self, report_data):
        self.report_data = report_data

    def data(self):
        return self.report_data

    def to_json(self):
        return json.dumps(self.report_data)

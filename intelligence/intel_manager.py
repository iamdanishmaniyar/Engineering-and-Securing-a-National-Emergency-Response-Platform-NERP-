"""
NERP Intelligence Service
Manages national security intelligence reports and suspect tracking.
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'datastore', 'intelligence.json')

class IntelManager:
    def __init__(self):
        self.reports = {}
        self.load_intelligence()

    def load_intelligence(self):
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                for rep in json.load(f):
                    self.reports[rep['reportId']] = rep

    def get_report(self, report_id):
        return self.reports.get(report_id, None)

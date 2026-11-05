"""
NERP Incidents Service
Loads, manages, and updates incident tickets from datastore.
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'datastore', 'incidents.json')

class IncidentManager:
    def __init__(self):
        self.incidents = {}
        self.load_incidents()

    def load_incidents(self):
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                for inc in json.load(f):
                    self.incidents[inc['incidentId']] = inc

    def get_incident(self, incident_id):
        return self.incidents.get(incident_id, None)

    def update_status(self, incident_id, updates):
        if incident_id in self.incidents:
            self.incidents[incident_id].update(updates)
            return True
        return False

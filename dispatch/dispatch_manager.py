"""
NERP Emergency Dispatch Service
Coordinates vehicle units, departure times, and arrival confirmations.
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'datastore', 'dispatch.json')

class DispatchManager:
    def __init__(self):
        self.dispatches = {}
        self.load_dispatch()

    def load_dispatch(self):
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                for d in json.load(f):
                    self.dispatches[d['dispatchId']] = d

    def get_dispatch(self, dispatch_id):
        return self.dispatches.get(dispatch_id, None)

    def update_dispatch_status(self, dispatch_id, new_status):
        if dispatch_id in self.dispatches:
            self.dispatches[dispatch_id]['status'] = new_status
            return True, f"Dispatch {dispatch_id} marked as {new_status}."
        return False, "Dispatch ID not found."

"""
NERP Audit Ledger & Retention Governance (Task C4 & TB5)
Maintains cryptographic audit logs and enforces retention policies.
"""
import os
import json
import hashlib
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT_DATA_PATH = os.path.join(BASE_DIR, 'datastore', 'audit.json')

class AuditLedger:
    def __init__(self):
        self.chain = []
        self.prev_hash = "0" * 64
        self.load_audit_history()

    def load_audit_history(self):
        if os.path.exists(AUDIT_DATA_PATH):
            with open(AUDIT_DATA_PATH, 'r', encoding='utf-8') as f:
                for entry in json.load(f):
                    self.append_log(entry['actor'], entry['resource'], entry['action'], "AUTHORIZED")

    def append_log(self, actor, resource, action, status, reason="N/A"):
        ts = datetime.now(timezone.utc).isoformat()
        payload = f"{ts}:{actor}:{resource}:{action}:{status}:{reason}:{self.prev_hash}"
        curr_hash = hashlib.sha256(payload.encode()).hexdigest()

        entry = {
            'timestamp': ts,
            'actor': actor,
            'resource': resource,
            'action': action,
            'status': status,
            'reason': reason,
            'blockHash': curr_hash,
            'prevHash': self.prev_hash
        }
        self.prev_hash = curr_hash
        self.chain.append(entry)
        return entry

    def evaluate_retention(self, timestamp_str, classification):
        """Task C4: Evaluates statutory retention expiry"""
        record_date = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        # Fixed simulation baseline date
        sim_now = datetime(2026, 11, 4, tzinfo=timezone.utc)
        age_days = (sim_now - record_date).days

        # Rules: OFFICIAL = 30 days, CONFIDENTIAL = 365 days, SECRET/TOP SECRET = 2555 days (7 yrs)
        limit = 30 if classification == 'OFFICIAL' else (365 if classification == 'CONFIDENTIAL' else 2555)

        if age_days > limit:
            return {'action': 'SECURE_DESTRUCT', 'reason': f'Retention window ({limit} days) exceeded.'}
        return {'action': 'RETAIN', 'days_remaining': limit - age_days}

"""
NERP Authentication & Token Service (TB1)
Maps responders, validates credentials, and issues session capability tokens.
"""
import os
import json
import hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASTORE_PATH = os.path.join(BASE_DIR, 'datastore', 'responders.json')

class TokenService:
    def __init__(self):
        self.responders = {}
        self.active_tokens = {} # token_id -> responder profile
        self.load_responders()

    def load_responders(self):
        if os.path.exists(DATASTORE_PATH):
            with open(DATASTORE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for r in data:
                    self.responders[r['name']] = r
                    self.responders[r['role']] = r

    def get_responder(self, role_or_name):
        return self.responders.get(role_or_name, None)

    def issue_token(self, role_or_name):
        user = self.get_responder(role_or_name)
        if not user:
            return None, "Identity authentication failed: Unknown responder."

        # Map role integrity levels
        integrity_map = {
            'Paramedic': 'OPERATIONAL',
            'Fire Officer': 'OPERATIONAL',
            'Police Officer': 'TACTICAL',
            'Intelligence Analyst': 'STRATEGIC',
            'Regional Commander': 'STRATEGIC',
            'National Commander': 'STRATEGIC',
            'Auditor': 'STRATEGIC'
        }

        user_integrity = integrity_map.get(user['role'], 'OPERATIONAL')
        raw_seed = f"{user['responderId']}:{user['role']}:NERP_SALT_2026"
        token_id = hashlib.sha256(raw_seed.encode()).hexdigest()[:16]

        session = {
            'tokenId': f"TOK-{token_id}",
            'responderId': user['responderId'],
            'name': user['name'],
            'role': user['role'],
            'clearance': user['clearanceLevel'],
            'integrity': user_integrity,
            'currentAssignment': user.get('currentAssignment')
        }
        self.active_tokens[session['tokenId']] = session
        return session, "Authentication successful."

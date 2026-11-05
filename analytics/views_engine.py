"""
NERP Analytics & Information Flow Views Engine (Task C3)
Generates Operational, Analytics, and Anonymised Research Views.
"""
import json
import hashlib

class ViewsEngine:
    @staticmethod
    def generate_operational_view(incident, responder_role="Paramedic"):
        inc_id = incident.get('incidentId') or incident.get('id') or 'RECORD-REF'
        location = incident.get('location') or 'Regional Sector - UK SW'
        inc_type = incident.get('incidentType') or incident.get('name') or 'Emergency Event'
        priority = incident.get('priority') or incident.get('classification') or 'High'
        agency = incident.get('assignedAgency') or 'Police / Ambulance / Fire'
        casualties = incident.get('casualties', 0)
        ts = incident.get('timestamp') or '2026-11-03T12:00:00Z'

        view = {
            'incidentId': inc_id,
            'timestamp': ts,
            'location': location,
            'incidentType': inc_type,
            'priority': priority,
            'assignedAgency': agency,
            'casualties': casualties
        }
        
        # Only police retain direct caller contact details
        if responder_role == 'Police Officer':
            view['callerName'] = incident.get('callerName') or incident.get('caller') or 'Direct Caller'
            view['callerPhone'] = incident.get('callerPhone') or '07700110000'
        else:
            view['callerName'] = '[REDACTED_PRIVACY_SENSITIVE]'
            view['callerPhone'] = '[REDACTED]'
        return view

    @staticmethod
    def generate_analytics_view(incident):
        inc_id = incident.get('incidentId') or incident.get('id') or 'RECORD-REF'
        ts = incident.get('timestamp') or '2026-11-03T12:00:00Z'
        location = incident.get('location') or 'Regional Sector - UK SW'
        inc_type = incident.get('incidentType') or incident.get('name') or 'Emergency Event'
        priority = incident.get('priority') or incident.get('classification') or 'High'
        casualties = incident.get('casualties', 0)

        return {
            'incidentId': inc_id,
            'timeBucket': ts[11:13] + ":00" if len(ts) >= 13 else "12:00",
            'generalArea': location,
            'incidentType': inc_type,
            'priority': priority,
            'casualties': casualties
        }

    @staticmethod
    def generate_research_view(incident):
        inc_id = incident.get('incidentId') or incident.get('id') or 'RECORD-REF'
        ts = incident.get('timestamp') or '2026-11-03T12:00:00Z'
        inc_type = incident.get('incidentType') or incident.get('name') or 'Emergency Event'
        priority = incident.get('priority') or incident.get('classification') or 'High'

        salt = "NERP_ACADEMIC_RESEARCH_SALT_2026"
        token = hashlib.sha256((str(inc_id) + salt).encode()).hexdigest()[:10]
        return {
            'researchToken': f"RES-{token}",
            'month': ts[:7] if len(ts) >= 7 else "2026-11",
            'category': inc_type,
            'severityBand': priority
        }

def show_data_views(incident_dict, user_role="Paramedic"):
    op = ViewsEngine.generate_operational_view(incident_dict, user_role)
    an = ViewsEngine.generate_analytics_view(incident_dict)
    res = ViewsEngine.generate_research_view(incident_dict)

    title_id = incident_dict.get('incidentId') or incident_dict.get('id') or 'RESOURCE'
    print(f"\n--- [PART C3] INFORMATION GOVERNANCE VIEWS FOR {title_id} ---")
    print("\n1. RAW PRIMARY DATASTORE RECORD:")
    print(json.dumps(incident_dict, indent=2))
    print(f"\n2. OPERATIONAL VIEW (Role: {user_role}):")
    print(json.dumps(op, indent=2))
    print("\n3. ANALYTICS VIEW (Operational Planning):")
    print(json.dumps(an, indent=2))
    print("\n4. RESEARCH VIEW (Anonymised Academic):")
    print(json.dumps(res, indent=2))

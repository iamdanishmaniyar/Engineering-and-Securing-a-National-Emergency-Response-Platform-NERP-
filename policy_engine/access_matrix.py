"""
Task D1: Operational Access Control Matrix (ACM)
Defines discretionary permissions per agency role across all four domains.
"""
ACM_RULES = {
    'Paramedic': {
        'incidents': ['READ', 'UPDATE'],
        'dispatch': ['READ'],
        'intelligence': [],
        'audit': []
    },
    'Fire Officer': {
        'incidents': ['READ', 'UPDATE', 'CLOSE'],
        'dispatch': ['READ'],
        'intelligence': [],
        'audit': []
    },
    'Police Officer': {
        'incidents': ['CREATE', 'READ', 'UPDATE'],
        'dispatch': ['READ'],
        'intelligence': ['READ'],
        'audit': []
    },
    'Intelligence Analyst': {
        'incidents': ['READ'],
        'dispatch': ['READ'],
        'intelligence': ['CREATE', 'READ', 'UPDATE'],
        'audit': []
    },
    'Regional Commander': {
        'incidents': ['CREATE', 'READ', 'UPDATE', 'DELETE', 'ARCHIVE'],
        'dispatch': ['READ', 'UPDATE'],
        'intelligence': ['READ', 'UPDATE'],
        'audit': ['READ']
    },
    'National Commander': {
        'incidents': ['READ', 'UPDATE'],
        'dispatch': ['READ'],
        'intelligence': ['READ'],
        'audit': ['READ']
    },
    'Auditor': {
        'incidents': ['READ'],
        'dispatch': ['READ'],
        'intelligence': ['READ'],
        'audit': ['READ']
    }
}

def check_acm(role, resource_type, action):
    allowed = ACM_RULES.get(role, {}).get(resource_type, [])
    if action in allowed:
        return True, "ACM authorization granted."
    return False, f"ACM Violation: Role '{role}' lacks operational '{action}' access on '{resource_type}'."

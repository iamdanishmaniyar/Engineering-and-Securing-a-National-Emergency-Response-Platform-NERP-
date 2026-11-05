"""
Task D2: Bell-LaPadula Confidentiality Model
Enforces Simple Security (No Read Up) and *-Property (No Write Down).
"""
CLEARANCE_ORDER = {
    'OFFICIAL': 1,
    'CONFIDENTIAL': 2,
    'SECRET': 3,
    'TOP SECRET': 4
}

def check_bell_lapadula(user_clearance, resource_classification, action):
    u_level = CLEARANCE_ORDER.get(user_clearance, 1)
    r_level = CLEARANCE_ORDER.get(resource_classification, 1)

    if action == 'READ':
        # Simple Security Property: No Read Up
        if u_level < r_level:
            return False, f"Bell-LaPadula 'No Read Up' failed: User ({user_clearance}) < Resource ({resource_classification})."
        return True, "Bell-LaPadula No Read Up satisfied."

    elif action in ['WRITE', 'CREATE', 'UPDATE', 'DELETE']:
        # *-Property: No Write Down
        if u_level > r_level:
            return False, f"Bell-LaPadula '*-Property (No Write Down)' failed: User ({user_clearance}) > Resource ({resource_classification}). Leakage hazard!"
        return True, "Bell-LaPadula No Write Down satisfied."

    return True, "BLP check passed."

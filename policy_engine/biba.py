"""
Task D3: Biba Strict Integrity Model
Enforces Simple Integrity (No Read Down) and Integrity *-Property (No Write Up).
"""
INTEGRITY_ORDER = {
    'UNTRUSTED': 1,
    'LOW': 1,
    'OPERATIONAL': 2,
    'MEDIUM': 2,
    'TACTICAL': 3,
    'HIGH': 3,
    'STRATEGIC': 4,
    'CRITICAL': 4
}

def check_biba(user_integrity, resource_integrity, action):
    u_int = INTEGRITY_ORDER.get(user_integrity, 1)
    r_int = INTEGRITY_ORDER.get(resource_integrity, 1)

    if action == 'READ':
        # Strict Integrity: No Read Down
        if u_int > r_int:
            return False, f"Biba 'No Read Down' failed: Subject ({user_integrity}) cannot ingest lower integrity ({resource_integrity}) data. Contamination hazard!"
        return True, "Biba No Read Down satisfied."

    elif action in ['WRITE', 'CREATE', 'UPDATE', 'DELETE']:
        # Integrity *-Property: No Write Up
        if u_int < r_int:
            return False, f"Biba 'No Write Up' failed: Subject integrity ({user_integrity}) < Target integrity ({resource_integrity})."
        return True, "Biba No Write Up satisfied."

    return True, "Biba check passed."

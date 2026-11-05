"""
Task D4: Unified Policy Decision Point (PDP)
Integrates ACM, Bell-LaPadula, and Biba into complete-mediation evaluation.
"""
from access_matrix import check_acm
from bell_lapadula import check_bell_lapadula
from biba import check_biba

ROLES = {
    'Paramedic': {'clearance': 'OFFICIAL', 'integrity': 'OPERATIONAL'},
    'Fire Officer': {'clearance': 'OFFICIAL', 'integrity': 'OPERATIONAL'},
    'Police Officer': {'clearance': 'SECRET', 'integrity': 'TACTICAL'},
    'Intelligence Analyst': {'clearance': 'TOP SECRET', 'integrity': 'STRATEGIC'},
    'Regional Commander': {'clearance': 'TOP SECRET', 'integrity': 'STRATEGIC'}
}

FILES = {
    'INC-001': {'name': 'Bristol Suspicious Package', 'type': 'incidents', 'classification': 'OFFICIAL', 'integrity': 'HIGH', 'caller': 'Alice Turner'},
    'INC-010': {'name': 'Cheltenham Terrorism Threat', 'type': 'incidents', 'classification': 'SECRET', 'integrity': 'HIGH', 'caller': 'Leo Ward'},
    'INT-005': {'name': 'National Transport Sabotage Plan', 'type': 'intelligence', 'classification': 'TOP SECRET', 'integrity': 'STRATEGIC', 'suspect': 'SUBJ-501'},
    'UNVERIFIED-LEAK': {'name': 'Social Media Rumour Feed', 'type': 'intelligence', 'classification': 'OFFICIAL', 'integrity': 'UNTRUSTED'}
}

def evaluate_access(role_name, file_key, action):
    role = ROLES[role_name]
    f_obj = FILES[file_key]

    print(f"\n[PDP EVALUATION] Subject: {role_name} (Clearance: {role['clearance']}, Integrity: {role['integrity']})")
    print(f"                 Resource: {file_key} (Class: {f_obj['classification']}, Integrity: {f_obj['integrity']}, Action: {action})")

    # Layer 1: ACM Check
    acm_ok, acm_msg = check_acm(role_name, f_obj['type'], action)
    if not acm_ok:
        return False, acm_msg
    print("  -> Layer 1: Access Control Matrix (ACM) PASSED.")

    # Layer 2: Bell-LaPadula Check
    blp_ok, blp_msg = check_bell_lapadula(role['clearance'], f_obj['classification'], action)
    if not blp_ok:
        return False, blp_msg
    print("  -> Layer 2: Bell-LaPadula Confidentiality PASSED.")

    # Layer 3: Biba Integrity Check
    biba_ok, biba_msg = check_biba(role['integrity'], f_obj['integrity'], action)
    if not biba_ok:
        return False, biba_msg
    print("  -> Layer 3: Biba Integrity PASSED.")

    return True, "All security policies satisfied. Operation authorized."

#!/usr/bin/env python3
"""
National Emergency Response Platform (NERP) - CLI Operational System
COMSM0122: Fundamentals of System Security - Group 2
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

search_paths = [
    BASE_DIR,
    os.path.join(BASE_DIR, 'consensus'),
    os.path.join(BASE_DIR, 'consensus', 'bft'),
    os.path.join(BASE_DIR, 'consensus', 'paxos'),
    os.path.join(BASE_DIR, 'consensus', 'raft'),
    os.path.join(BASE_DIR, 'experiments'),
    os.path.join(BASE_DIR, 'experiments', 'bft'),
    os.path.join(BASE_DIR, 'experiments', 'paxos'),
    os.path.join(BASE_DIR, 'experiments', 'raft'),
    os.path.join(BASE_DIR, 'policy_engine'),
    os.path.join(BASE_DIR, 'policy-engine'),
    os.path.join(BASE_DIR, 'analytics'),
    os.path.join(BASE_DIR, 'audit'),
    os.path.join(BASE_DIR, 'auth'),
    os.path.join(BASE_DIR, 'incidents'),
    os.path.join(BASE_DIR, 'dispatch'),
    os.path.join(BASE_DIR, 'intelligence')
]

for p in search_paths:
    if p not in sys.path and os.path.exists(p):
        sys.path.insert(0, p)

from pdp import evaluate_access, ROLES, FILES
from views_engine import show_data_views
from audit_ledger import AuditLedger

def run_experiment_script(filename):
    possible_dirs = [
        os.path.join(BASE_DIR, 'experiments'),
        os.path.join(BASE_DIR, 'experiments', 'bft'),
        os.path.join(BASE_DIR, 'experiments', 'paxos'),
        os.path.join(BASE_DIR, 'experiments', 'raft'),
        os.path.join(BASE_DIR, 'consensus'),
        os.path.join(BASE_DIR, 'consensus', 'bft'),
        os.path.join(BASE_DIR, 'consensus', 'paxos'),
        os.path.join(BASE_DIR, 'consensus', 'raft'),
        os.path.join(BASE_DIR, 'consensus', 'b5_experiment'),
        BASE_DIR
    ]
    target_path = None
    for d in possible_dirs:
        test_file = os.path.join(d, filename)
        if os.path.exists(test_file):
            target_path = test_file
            break

    if not target_path:
        print(f"\n[ERROR] Could not find '{filename}'. Check its location.")
        return

    print(f"\n>>> Running: {os.path.basename(target_path)} ...\n")
    pythonpath_entries = [
        BASE_DIR,
        os.path.join(BASE_DIR, 'consensus'),
        os.path.join(BASE_DIR, 'consensus', 'bft'),
        os.path.join(BASE_DIR, 'consensus', 'paxos'),
        os.path.join(BASE_DIR, 'consensus', 'raft'),
        os.path.join(BASE_DIR, 'consensus', 'b5_experiment'),
        os.path.dirname(target_path)
    ]
    cmd = f'PYTHONPATH="{":".join(pythonpath_entries)}" python3 "{target_path}"'
    os.system(cmd)

def menu_access_control():
    print("\n--- [PART D] Access Control & Multi-Layer Policy Lab ---")
    print("Roles: 1) Paramedic  2) Fire Officer  3) Police Officer  4) Intelligence Analyst  5) Regional Commander")
    r_choice = input("Select Role (1-5): ").strip()
    role_keys = list(ROLES.keys())
    role = role_keys[int(r_choice) - 1] if r_choice in ['1', '2', '3', '4', '5'] else 'Paramedic'

    print("\nTarget Files:")
    file_keys = list(FILES.keys())
    for idx, k in enumerate(file_keys):
        print(f"  {idx + 1}) {k} [Class: {FILES[k]['classification']}, Integrity: {FILES[k]['integrity']}]")
    f_choice = input("Select File (1-4): ").strip()
    file_key = file_keys[int(f_choice) - 1] if f_choice in ['1', '2', '3', '4'] else 'INC-001'

    print("\nActions: 1) READ  2) UPDATE  3) DELETE")
    a_choice = input("Select Action (1-3): ").strip()
    actions = ['READ', 'UPDATE', 'DELETE']
    action = actions[int(a_choice) - 1] if a_choice in ['1', '2', '3'] else 'READ'

    granted, msg = evaluate_access(role, file_key, action)
    print(f"\n>>> FINAL VERDICT: {'[ACCESS GRANTED]' if granted else '[ACCESS BLOCKED]'}")
    print(f">>> Details: {msg}")

def menu_consensus_attacks():
    while True:
        print("\n--- [PART B] Distributed Consensus Attacks & Failures ---")
        print("1)  BFT: Equivocation Attack (Double-Voting)")
        print("2)  BFT: Sybil Attack (Unapproved Node Flooding)")
        print("3)  BFT: Validator Key Compromise & Revocation")
        print("4)  Paxos: State Loss (Volatile Disk Crash)")
        print("5)  Paxos: Majority Loss (Cluster Stall)")
        print("6)  Paxos: Quorum Misconfiguration (Split-Brain)")
        print("7)  Raft: Network Partition (Split-Brain Isolation)")
        print("8)  Raft: Election Storm (Concurrent Timeout Loop)")
        print("9)  Raft: Leadership Churn (Frequent Leader Crashes)")
        print("10) Task B5: Original Hardening (Threshold Key Signatures)")
        print("11) Back to Main Menu")

        choice = input("\nSelect Scenario (1-11): ").strip()
        if choice == '1': run_experiment_script("equivocation.py")
        elif choice == '2': run_experiment_script("sybil.py")
        elif choice == '3': run_experiment_script("key_compromise.py")
        elif choice == '4': run_experiment_script("state_loss.py")
        elif choice == '5': run_experiment_script("majority_loss.py")
        elif choice == '6': run_experiment_script("quorum_misconfig.py")
        elif choice == '7': run_experiment_script("network_partition.py")
        elif choice == '8': run_experiment_script("election_storm.py")
        elif choice == '9': run_experiment_script("leadership_churn.py")
        elif choice == '10': run_experiment_script("threshold_hardening.py")
        elif choice == '11': break
        else: print("Invalid choice, choose 1-11.")

def menu_retention_lifecycle():
    ledger = AuditLedger()
    print("\n--- [PART C4] Automated Retention Lifecycle & Cryptographic Destruction ---")
    print("1) Evaluate Active Record (INC-001 | OFFICIAL - 30-day limit)")
    print("2) Evaluate Classified Record (INC-010 | SECRET - 7-year limit)")
    print("3) Simulate Expired Record Destruction (Overdue OFFICIAL Record)")

    c = input("\nSelect Retention Test (1-3): ").strip()
    if c == '1':
        res = ledger.evaluate_retention("2026-11-03T10:15:00Z", "OFFICIAL")
        print(f"\n>>> [RETENTION STATUS: {res['action']}] Active window intact ({res['days_remaining']} days remaining).")
    elif c == '2':
        res = ledger.evaluate_retention("2026-11-03T12:50:00Z", "SECRET")
        print(f"\n>>> [RETENTION STATUS: {res['action']}] National security statutory hold active ({res['days_remaining']} days remaining).")
    elif c == '3':
        res = ledger.evaluate_retention("2026-08-01T10:00:00Z", "OFFICIAL")
        print(f"\n>>> [POLICY TRIGGERED: {res['action']}] {res['reason']}")
        entry = ledger.append_log("SYSTEM_SHREDDER", "OLD_INC_999", "CRYPTOGRAPHIC_KEY_DELETION", "SUCCESS", "Retention expired")
        print(f">>> [PROOF OF DESTRUCTION COMMITTED TO TB5 AUDIT LOG]")
        print(f"    Target Asset: OLD_INC_999")
        print(f"    Action      : Table Encryption Keys Purged")
        print(f"    Audit Hash  : {entry['blockHash']}")

def run_main():
    while True:
        print("\n" + "=" * 60)
        print("  NERP UK: NATIONAL EMERGENCY PLATFORM - SECURITY TESTBED   ")
        print("=" * 60)
        print("1. [Part D] Test Multi-Layer Access Control (BLP + Biba + ACM)")
        print("2. [Part B] Test Distributed Consensus Failures & Attacks")
        print("3. [Part C] Inspect Data Governance Views (Operational / Research)")
        print("4. [Part C] Test Automated Retention Lifecycle & Destruction (Task C4)")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()
        if choice == '1':
            menu_access_control()
        elif choice == '2':
            menu_consensus_attacks()
        elif choice == '3':
            files = list(FILES.keys())
            for i, f in enumerate(files):
                print(f"  {i + 1}) {f}")
            c = input("Select Record (1-4): ").strip()
            sel_key = files[int(c) - 1] if c in ['1', '2', '3', '4'] else 'INC-001'
            record = dict(FILES[sel_key])
            record['id'] = sel_key
            record['incidentId'] = sel_key
            show_data_views(record)
        elif choice == '4':
            menu_retention_lifecycle()
        elif choice == '5':
            print("\nExiting NERP system.")
            break
        else:
            print("Invalid choice, choose 1-5.")

run_main()

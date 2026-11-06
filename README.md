# National Emergency Response Platform (NERP)
### COMSM0122: Fundamentals of System Security — Group 2 Prototype
**Infrastructure Security Pathway | University of Bristol**

---

## 1. Executive Overview

The **National Emergency Response Platform (NERP)** is a mission-critical distributed platform designed to coordinate UK emergency responders (Police, Fire and Rescue, Ambulance services), regional command centres, and national counter-terrorism intelligence coordinators. 

This repository contains the prototype implementation, adversarial consensus attack simulations, data governance engines, and the multi-layer security policy decision engine developed in compliance with the **COMSM0122 System Security Coursework Specification**.

### Key Architectural Tenets
* **Native, Zero-Dependency Implementation:** Developed entirely in native Python 3 with standard libraries (`hashlib`, `json`, `datetime`, `os`, `sys`). No third-party packages or virtual environment installations are required.
* **Separation of Concerns:** Rigidly structured into modular domain subsystems (`auth/`, `incidents/`, `dispatch/`, `intelligence/`, `analytics/`, `audit/`, `consensus/`, `policy_engine/`, and `experiments/`).
* **Multi-Layer Complete Mediation:** Access requests are evaluated sequentially through an Access Control Matrix (ACM), Bell-LaPadula Confidentiality Lattice, and Biba Strict Integrity Model.
* **Adversarial Resilience:** Demonstrates distributed consensus under active attack (equivocation, Sybil floods, validator key compromise, state amnesia, network partitions, split-brain scenarios, and election storms), reinforced by an original $(t=2, n=3)$ threshold signature hardening mechanism.

---

## 2. Directory & Component Structure

The repository is organized according to the architecture specified in the coursework specification:

```text
nerp/
├── main.py                           # Root interactive CLI evaluation harness
├── README.md                         # Operational & architectural documentation
│
├── datastore/                        # Primary ingested JSON datasets
│   ├── incidents.json                # Emergency incident records
│   ├── responders.json               # Active duty responder profiles & clearances
│   ├── intelligence.json             # Counter-terrorism & threat dossiers
│   ├── dispatch.json                 # Emergency vehicle dispatch statuses
│   └── audit.json                    # Historical system audit events
│
├── auth/                             # Trust Boundary 1 (Authentication & Capabilities)
│   └── token_service.py              # Identity verification & capability token minting
│
├── incidents/                        # Operational Incident Subsystem
│   └── incident_manager.py           # Ingestion, status lifecycle, and record retrieval
│
├── dispatch/                         # Operational Dispatch Subsystem
│   └── dispatch_manager.py           # Unit allocation and vehicle tracking
│
├── intelligence/                     # Intelligence Distribution Subsystem
│   └── intel_manager.py              # Classified national threat dossier management
│
├── analytics/                        # Task C3: Information Flow Engineering
│   └── views_engine.py               # Operational, Analytics, and Research View transforms
│
├── audit/                            # Task C4 & TB5: Tamper-Evident Ledger
│   └── audit_ledger.py               # Cryptographic hash-chained audit log & crypto-shredding
│
├── consensus/                        # Protocol Core Engines (Part B)
│   ├── bft/
│   │   └── bft_common.py             # Byzantine node primitives & validator registry
│   ├── paxos/
│   │   └── paxos_common.py           # Acceptor, proposer, and disk persistence models
│   └── raft/
│       └── raft_common.py            # Raft node, cluster coordinator, and term state machine
│
├── policy_engine/                    # Part D: Multi-Layer Policy Decision Point (PDP)
│   ├── access_matrix.py              # Task D1: Domain-specific operational role permissions
│   ├── bell_lapadula.py              # Task D2: Simple Security & *-Property enforcement
│   ├── biba.py                       # Task D3: Strict Integrity & *-Property enforcement
│   └── pdp.py                        # Task D4: Unified complete mediation evaluator
│
└── experiments/                      # Adversarial Attack & Failure Simulations
    ├── bft/
    │   ├── equivocation.py           # Task B4.1: Double-voting Byzantine attack
    │   ├── sybil.py                  # Task B4.1: Unapproved identity flood
    │   ├── key_compromise.py         # Task B4.1: Private key theft, rotation, & revocation
    │   └── threshold_hardening.py    # Task B5: Original (t=2, n=3) threshold signature defense
    ├── paxos/
    │   ├── state_loss.py             # Task B4.2: Volatile crash / disk amnesia
    │   ├── majority_loss.py          # Task B4.2: Majority acceptor outage & cluster stall
    │   └── quorum_misconfig.py       # Task B4.2: Split-brain under reduced majority
    └── raft/
        ├── network_partition.py      # Task B4.3: Minority isolation & recovery
        ├── election_storm.py         # Task B4.3: High-latency split-vote loops
        └── leadership_churn.py       # Task B4.3: Frequent leader failure throughput collapse
```

---

## 3. Quick Start & Execution

### Prerequisites
* Any standard UNIX, Linux, macOS, or Windows WSL terminal with **Python 3.8+** installed.
* Zero external package dependencies (`pip install` is **not** required).

### Running the Platform
Navigate to the root directory and launch the master test harness:

```bash
cd nerp/
python3 main.py
```

The system initializes with an interactive menu:
```text
==============================================================
  NERP UK: NATIONAL EMERGENCY PLATFORM - SECURITY TESTBED   
==============================================================
1. [Part D] Test Multi-Layer Access Control (BLP + Biba + ACM)
2. [Part B] Test Distributed Consensus Failures & Attacks
3. [Part C] Inspect Data Governance Views (Operational / Research)
4. [Part C] Test Automated Retention Lifecycle & Destruction (Task C4)
5. Exit
```

---

## 4. Operational Walkthrough & Test Scenarios

### Option 1: Multi-Layer Access Control Policy Lab (Part D)
Evaluates access requests across the sequential pipeline: **ACM $\rightarrow$ Bell-LaPadula $\rightarrow$ Biba**.

* **Scenario 1.1: ACM Authorization Failure (Role Violation)**
  * *Input:* Role `1` (Paramedic) $\rightarrow$ File `3` (`INT-005`) $\rightarrow$ Action `1` (`READ`)
  * *Result:* `ACCESS BLOCKED`
  * *Reason:* ACM Violation: Role 'Paramedic' lacks operational access to the `intelligence` domain.
* **Scenario 1.2: Bell-LaPadula Failure ("No Read Up" — Task D4.1)**
  * *Input:* Role `1` (Paramedic, Clearance: `OFFICIAL`) $\rightarrow$ File `2` (`INC-010`, Class: `SECRET`) $\rightarrow$ Action `1` (`READ`)
  * *Result:* `ACCESS BLOCKED`
  * *Reason:* Bell-LaPadula Simple Security violation: User clearance (`OFFICIAL`) < File classification (`SECRET`).
* **Scenario 1.3: Biba Integrity Failure ("No Read Down" — Task D4.2)**
  * *Input:* Role `5` (Regional Commander, Integrity: `STRATEGIC`) $\rightarrow$ File `4` (`UNVERIFIED-LEAK`, Integrity: `UNTRUSTED`) $\rightarrow$ Action `1` (`READ`)
  * *Result:* `ACCESS BLOCKED`
  * *Reason:* Biba Simple Integrity violation: Strategic subject cannot ingest untrusted data (data poisoning hazard).
* **Scenario 1.4: Bell-LaPadula Failure ("*-Property / No Write Down")**
  * *Input:* Role `4` (Intelligence Analyst, Clearance: `TOP SECRET`) $\rightarrow$ File `1` (`INC-001`, Class: `OFFICIAL`) $\rightarrow$ Action `2` (`UPDATE`)
  * *Result:* `ACCESS BLOCKED`
  * *Reason:* Bell-LaPadula $\star$-Property violation: High-clearance subject cannot write into lower-classified files (covert exfiltration hazard).
* **Scenario 1.5: Full Authorization Pass (Task D4.3)**
  * *Input:* Role `4` (Intelligence Analyst) $\rightarrow$ File `3` (`INT-005`, Class: `TOP SECRET`, Integrity: `STRATEGIC`) $\rightarrow$ Action `1` (`READ`)
  * *Result:* `ACCESS GRANTED`
  * *Reason:* ACM, Bell-LaPadula, and Biba properties are all satisfied simultaneously.

---

### Option 2: Distributed Consensus & Adversarial Attacks (Part B)
Directly triggers the standalone attack simulations in `experiments/`:

1. **BFT Equivocation (Task B4.1):** Simulates Byzantine Node D double-voting for conflicting values (100 and 50). Signature cross-validation detects the conflict and excludes Node D from quorum.
2. **BFT Sybil Attack (Task B4.1):** Floods the cluster with unapproved nodes (`X1`–`X5`). The cryptographic validator registry isolates and drops unauthenticated votes.
3. **BFT Key Compromise (Task B4.1):** Simulates private key theft (`KEY1`), subsequent anomalous voting, dynamic key rotation (`KEY2`), and Certificate Revocation List (CRL) blacklisting.
4. **Paxos State Loss (Task B4.2):** Acceptor `A1` crashes and loses in-memory promises due to omitted disk sync (`fsync`), allowing an obsolete proposal to overwrite committed state.
5. **Paxos Majority Loss (Task B4.2):** Acceptors `A3`, `A4`, and `A5` fail simultaneously. Proposer `P1` cannot reach majority (2/5 votes), stalling the cluster to preserve safety.
6. **Paxos Quorum Misconfiguration (Task B4.2):** Quorum requirement lowered from 3 to 2 on a 5-node cluster, eliminating mathematical intersection and inducing split-brain divergence.
7. **Raft Network Partition (Task B4.3):** Isolates the leader into a minority partition where commits fail. The majority partition elects a new term leader, and the old leader reconciles upon recovery.
8. **Raft Election Storm (Task B4.3):** Simulates high network latency causing concurrent election timeouts, self-voting loops, and total loss of liveness.
9. **Raft Leadership Churn (Task B4.3):** Rapid crash cycles of newly elected leaders reduce operational write throughput to zero.
10. **Task B5 Original Hardening (Threshold Signatures):** Splits the signing key into $(t=2, n=3)$ shares using Shamir's Secret Sharing. Shows that an adversary holding a single stolen share is mathematically incapable of forging consensus.

---

### Option 3: Information Governance Views (Part C3)
Demonstrates multi-tier data flow transformations on ingested incidents:
* **Raw Datastore:** Preserves primary schema with full caller PII and exact operational coordinates.
* **Operational View:** Supplies field responders with tactical dispatch metadata while suppressing caller PII to `[REDACTED_PRIVACY_SENSITIVE]`.
* **Analytics View:** Generalizes coordinates to regional boundaries and coarsens timestamps into 1-hour intervals (`12:00`) for capacity planning.
* **Research View ($k$-Anonymity):** Anonymizes identifiers into irreversible SHA-256 salted tokens (`RES-8b6fa2018a`) and coarsens time to month granularity (`2026-11`).

---

### Option 4: Automated Retention Lifecycle & Crypto-Shredding (Task C4)
Simulates statutory retention schedules and data destruction:
* **Active OFFICIAL Record:** Evaluates 30-day retention rule (`INC-001`), confirming active status.
* **National Security Record:** Evaluates 7-year (2555-day) statutory retention hold (`INC-010`).
* **Expired Record Cryptographic Destruction:** Triggers automated crypto-shredding on overdue records, purging symmetric encryption keys and appending an immutable proof-of-destruction receipt into the tamper-evident audit ledger (TB5).

---

## 5. Security Architecture Mapping

| Trust Boundary / Subsystem | Primary Threat Addressed | Defense Mechanism Applied |
| :--- | :--- | :--- |
| **TB1: Public Ingestion** | DoS, Credential Forgery | Rate limiting, Session capability tokens |
| **TB2: Policy Enforcement** | Privilege Escalation, Exfiltration, Data Contamination | Multi-layer PDP: ACM + Bell-LaPadula + Biba |
| **TB3: Distributed Consensus** | Byzantine Validators, Split-Brain, Network Partition | Raft (Crash faults), Paxos (Allocation), PBFT (Adversarial) |
| **TB4: Primary Datastores** | Unauthorized Rest Access, Premature Exposure | Transparent encryption, 3-tier view sanitization |
| **TB5: National Audit Log** | Audit Repudiation, Forensic Tampering | Append-only SHA-256 hash-chained ledger |

---

## 6. Authors & Coursework Metadata
* **Course:** COMSM0122: Fundamentals of System Security
* **Group:** Group 2 (Infrastructure Security Pathway)
* **Academic Year:** 2026
* **Institution:** University of Bristol
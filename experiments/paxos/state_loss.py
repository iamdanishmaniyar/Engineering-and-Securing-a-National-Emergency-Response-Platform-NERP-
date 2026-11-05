from paxos_common import Acceptor

def run_state_loss():
    print("=== Paxos State Loss ===")
    a1 = Acceptor("A1")
    a2 = Acceptor("A2")
    a3 = Acceptor("A3")
    acceptors = [a1, a2, a3]
    print("[INFO] Phase 1 & 2: Proposer P1 proposes value 'instances=10' with ID 5.")
    for a in acceptors:
        a.prepare(5)
        a.accept(5, "instances=10")
    print(f"  [RESULT] Value COMMITTED. A1 holds: {a1.accepted_proposal}")

    print("[ACTION] Acceptor A1 crashes and loses its disk (State Loss).")
    a1.accepted_proposal = None
    a1.highest_promised = 0

    print("[ACTION] Proposer P2 proposes a different value 'instances=20' with ID 3.")
    print("  [INFO] Sending Prepare(3) to all acceptors...")
    a1.prepare(3)

    print("  [INFO] Sending Accept(3, 'instances=20') to A1...")
    a1.accept(3, "instances=20")

    print(f"[RESULT] A1 accepted new value: {a1.accepted_proposal}")
    print("[WARNING] Acceptor forgot previous history.")
    print("[CONCLUSION] Paxos safety assumption violated. A new proposal with lower number could overwrite the committed value.")

if __name__ == "__main__":
    run_state_loss()
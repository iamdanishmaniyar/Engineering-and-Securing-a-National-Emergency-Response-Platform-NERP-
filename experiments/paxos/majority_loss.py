from paxos_common import Acceptor, Proposer

def run_majority_loss():
    print("=== Paxos Majority Loss ===")
    p1 = Proposer("P1")
    nodes = [Acceptor(f"A{i}") for i in range(1, 6)]
    print(f"[INFO] Proposer P1 wants to commit 'instances=10'. Quorum required: 3.")

    print("[ACTION] Nodes A3, A4, A5 crash (offline).")
    online_nodes = [nodes[0], nodes[1]]
    votes = 0
    for a in online_nodes:
        if a.prepare(1):
            votes += 1

    print(f"  [RESULT] P1 received {votes} votes.")
    if votes >= 3:
        print("  [RESULT] Quorum reached. Committed.")
    else:
        print("  [RESULT] Consensus HALTED. Cannot reach quorum.")
        print("[CONCLUSION] Liveness lost (system stalled), but Safety preserved. No conflicting values can be committed.")

if __name__ == "__main__":
    run_majority_loss()
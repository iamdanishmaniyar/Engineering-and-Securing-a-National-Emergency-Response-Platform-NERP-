from paxos_common import Acceptor, Proposer
def run_quorum_misconfig():
    print("=== Paxos Quorum Misconfiguration ===")
    print("[INFO] System has 5 nodes. Correct quorum requirement is 3.")

    unsafe_quorum = 2
    print(f"[ACTION] Misconfiguration: Changing majority requirement to {unsafe_quorum}.")
    partition_1 = [Acceptor("A1"), Acceptor("A2")]
    partition_2 = [Acceptor("A4"), Acceptor("A5")]
    print("-[ACTION] Partition 1 receives proposal 'Value X' (ID=1)")
    votes_p1 = 0
    for a in partition_1:
        if a.accept(1, "Value_X"): votes_p1 += 1
    if votes_p1 >= unsafe_quorum:
        print(f"  [PARTITION 1] {votes_p1} votes >= Quorum(2). COMMITTED Value_X.")

    print("-[ACTION] Partition 2 receives proposal 'Value Y' (ID=2)")
    votes_p2 = 0
    for a in partition_2:
        if a.accept(2, "Value_Y"): votes_p2 += 1
    if votes_p2 >= unsafe_quorum:
        print(f"  [PARTITION 2] {votes_p2} votes >= Quorum(2). COMMITTED Value_Y.")

    print("[WARNING]: Split-Brain occurred. Both partitions committed different values independently.")
    print("[CONCLUSION] Quorum intersection removed, Safety violated. Different values could be chosen.")

if __name__ == "__main__":
    run_quorum_misconfig()
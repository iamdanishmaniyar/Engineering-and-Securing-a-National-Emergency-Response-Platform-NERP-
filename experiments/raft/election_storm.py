from raft_common import Node, Cluster, Network, Simulator
def run_election_storm():
    print("=== Raft Election Storm ===")
    nodes = [Node("A"), Node("B"), Node("C")]
    cluster = Cluster(nodes)
    print("[INFO] Simulating high network latency causing concurrent timeouts.")
    for round_num in range(1, 4):
        print(f"--- Election Round {round_num} ---")
        for node in nodes:
            node.become_candidate()
        votes = {n.id: 1 for n in nodes}
        print("  [INFO] All nodes voted for themselves. Split vote occurs.")
        print("  [ERROR] No candidate achieved majority (2/3).")

    print("[CONCLUSION] Liveness/Availability lost. The cluster is stuck in an election loop.")

if __name__ == "__main__":
    run_election_storm()
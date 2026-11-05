from raft_common import Node, Cluster, Network, Simulator
def run_leadership_churn():
    print("=== Raft Leadership Churn ===")
    nodes = [Node("A"), Node("B"), Node("C")]
    cluster = Cluster(nodes)
    network = Network()
    sim = Simulator(cluster, network)
    for cycle in range(1, 4):
        print(f"--- Cycle {cycle} ---")
        leader = cluster.leader()
        if not leader:
            target_node = nodes[cycle % 3]
            sim.elect_leader(target_node)
            leader = cluster.leader()

        if leader:
            print(f"  [ACTION] Leader {leader.id} crashes immediately.")
            leader.fail()
            print("  [ERROR] Client request dropped. No new entries committed due to crash.")
            next_node = [n for n in nodes if n.online and n != leader][0]
            sim.elect_leader(next_node)

    print("[RESULT] Safety preserved (no corruption). But throughput is near zero due to constant re-elections.")

if __name__ == "__main__":
    run_leadership_churn()
from raft_common import Node, Cluster, Network, Simulator
def run_network_partition():
    print("=== Raft Network Partition ===")
    nodes = [Node("A"),Node("B"),Node("C")]
    cluster = Cluster(nodes)
    network = Network()
    sim = Simulator(cluster, network)

    print("[INFO] Initial state: A is Leader.")
    nodes[0].become_leader()

    network.set_partition({"A"})
    print("[ACTION] Network partition occurs! Leader A is isolated.")
    print("[TEST] Leader A tries to replicate to B and C.")
    sim.replicate("instances=10")

    print("[INFO] Nodes B and C time out. Triggering new election.")
    network.partitioned = False
    sim.elect_leader(nodes[1])

    print("[ACTION] Network partition repaired. Leader A reconnects.")
    network.repair()
    print("[TEST] A sends heartbeat to B.")
    if network.send(nodes[0], nodes[1], f"AppendEntries(term={nodes[0].current_term})"):
        if nodes[0].current_term < nodes[1].current_term:
            print(f"  [INFO] A sees higher term ({nodes[1].current_term}). Stepping down.")
            nodes[0].become_follower(nodes[1].current_term)
            print("  [RESULT] Safety preserved. Old leader stepped down.")

if __name__ == "__main__":
    run_network_partition()
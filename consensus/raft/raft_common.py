class LogEntry:
    def __init__(self, index, term, command):
        self.index = index
        self.term = term
        self.command = command

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.role = "FOLLOWER"
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.online = True

    def become_follower(self, term):
        self.role = "FOLLOWER"
        self.current_term = term
        self.voted_for = None
        print(f"  [{self.id}] -> FOLLOWER (Term {self.current_term})")

    def become_candidate(self):
        self.role = "CANDIDATE"
        self.current_term += 1
        self.voted_for = self.id
        print(f"  [{self.id}] -> CANDIDATE (Term {self.current_term})")

    def become_leader(self):
        self.role = "LEADER"
        print(f"  [{self.id}] -> LEADER (Term {self.current_term})")

    def fail(self):
        self.online = False
        self.role = "FOLLOWER"
        print(f"  [{self.id}] OFFLINE (Crashed)")

    def recover(self):
        self.online = True
        print(f"  [{self.id}] ONLINE (Recovered)")

class Cluster:
    def __init__(self, nodes):
        self.nodes = nodes

    def majority(self):
        return (len(self.nodes) // 2) + 1

    def online_nodes(self):
        return [n for n in self.nodes if n.online]

    def has_majority(self):
        return len(self.online_nodes()) >= self.majority()

    def leader(self):
        for n in self.nodes:
            if n.role == "LEADER" and n.online:
                return n
        return None


class Network:
    def __init__(self):
        self.partitioned = False
        self.isolated_nodes = set()

    def set_partition(self, isolated_nodes):
        self.partitioned = True
        self.isolated_nodes = isolated_nodes
        print(f"  [NETWORK] Partition ACTIVE. Isolated: {isolated_nodes}")

    def repair(self):
        self.partitioned = False
        self.isolated_nodes = set()
        print("  [NETWORK] Partition REPAIRED.")

    def send(self, src_node, dst_node, message):
        if not src_node.online or not dst_node.online:
            return False
        if self.partitioned:
            if (src_node.id in self.isolated_nodes) or (dst_node.id in self.isolated_nodes):
                print(f"  [NETWORK DROPPED] {src_node.id} -> {dst_node.id}: {message}")
                return False
        print(f"  [NETWORK DELIVERED] {src_node.id} -> {dst_node.id}: {message}")
        return True

class Simulator:
    def __init__(self, cluster, network):
        self.cluster = cluster
        self.network = network

    def elect_leader(self, candidate):
        candidate.become_candidate()
        votes = 1
        print(f"  [{candidate.id}] Requesting votes for Term {candidate.current_term}...")
        for peer in self.cluster.nodes:
            if peer.id != candidate.id and peer.online:
                if self.network.send(candidate, peer, "RequestVote"):
                    votes += 1
        print(f"  [VOTES] {candidate.id} received {votes}/{len(self.cluster.nodes)} votes.")
        if votes >= self.cluster.majority():
            candidate.become_leader()
            return True
        return False

    def replicate(self, command):
        leader = self.cluster.leader()
        if not leader:
            print("  [ERROR] NO LEADER. Cannot replicate.")
            return
        entry = LogEntry(len(leader.log) + 1, leader.current_term, command)
        leader.log.append(entry)
        print(f"  [LEADER {leader.id}] Created entry: {command}")
        acks = 1
        for peer in self.cluster.nodes:
            if peer.id != leader.id and peer.online:
                if self.network.send(leader, peer, f"AppendEntries({command})"):
                    peer.log.append(entry)
                    acks += 1
        if acks >= self.cluster.majority():
            print("  [RESULT] ENTRY COMMITTED to majority.")
        else:
            print("  [ERROR] Failed to replicate to majority.")

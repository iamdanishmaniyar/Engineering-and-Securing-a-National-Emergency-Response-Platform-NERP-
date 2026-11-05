from bft_common import Node, sign
def run_sybil():
    print("=== BFT Sybil Attack ===")
    approved_nodes = {"A", "B", "C", "D"}
    print(f"[INFO] Approved validators in Registry: {approved_nodes}")

    fake_nodes = [Node(f"X{i}") for i in range(1, 6)]
    print("[WARN] Attacker generating 5 fake nodes (X1-X5) to flood the network.")
    all_votes = [Node("A").vote(100), Node("B").vote(100)]
    all_votes += [n.vote(50) for n in fake_nodes]
    all_votes += [Node("C").vote(100), Node("D").vote(100)]

    print("[INFO] Filtering votes...")
    valid_votes = []
    for v in all_votes:
        if v["sender"] not in approved_nodes:
            print(f"[REJECTED] Unapproved validator: {v['sender']}")
        elif v["sig"] != sign(v["sender"], v["value"]):
            print(f"[REJECTED] Invalid signature for {v['sender']}")
        else:
            valid_votes.append(v)

    quorum_required = 3
    print(f"[INFO] Valid votes received: {len(valid_votes)}. Quorum required: {quorum_required}")
    if len(valid_votes) >= quorum_required:
        print("[RESULT] Consensus reached safely. Sybil nodes ignored. Liveness preserved.")
    else:
        print("[RESULT] Consensus failed. (This should not happen here).")

if __name__ == "__main__":
    run_sybil()
from bft_common import Node, sign
def run_equivocation():
    print("=== BFT Equivocation Attack ===")
    honest_nodes = [Node("A"), Node("B"), Node("C")]
    print("[INFO] Honest nodes A, B, C are voting for value 100.")
    honest_votes = [n.vote(100) for n in honest_nodes]

    print("[WARN] Malicious node D is equivocating!")
    print("       -> Sending value 100 to A")
    print("       -> Sending value 50 to B")
    vote_to_A = {"sender": "D", "value": 100, "sig": sign("D",100)}
    vote_to_B = {"sender": "D", "value": 50, "sig": sign("D",50)}

    print("[INFO] Receiver validating messages...")
    seen_votes_from_D = set()
    for msg in [vote_to_A, vote_to_B]:
        msg_content = (msg["value"],msg["sig"])
        if msg_content in seen_votes_from_D:
            continue
        seen_votes_from_D.add(msg_content)
    valid_votes = list(honest_votes)
    if len(seen_votes_from_D) > 1:
        print("[ALERT] EQUIVOCATION DETECTED: Node D sent conflicting messages!")
        print("[ACTION] Node D signature rejected. Excluding D from quorum.")
    else:
        valid_votes.append(vote_to_A)

    quorum_required = 3
    print(f"[INFO] Total valid votes: {len(valid_votes)} (Required: {quorum_required})")
    if len(valid_votes) >= quorum_required:
        print("[RESULT] Consensus safe. Quorum reached by A, B, C. Integrity preserved.")
    else:
        print("[RESULT] Consensus failed. Not enough valid votes.")

if __name__ == "__main__":
    run_equivocation()
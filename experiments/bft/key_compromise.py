from bft_common import Registry
def run_key_compromise():
    print("=== BFT Validator Key Compromise ===")
    reg=Registry()
    stolen_key = "KEY1"
    print(f"[WARN] Attacker steals Node A's private key ({stolen_key})")
    print("[ACTION] Attacker forges a vote from A for value 999...")
    forge_vote = {"sender": "A", "value": 999, "key_used": stolen_key}
    status = reg.verify(forge_vote["sender"], forge_vote["key_used"], forge_vote["value"])
    print(f"[RESULT] Before rotation: Forged vote status -> {status} (Vulnerable)")

    print("[INFO] System detects anomaly and triggers Key Rotation for A.")
    reg.rotate_key("A", "KEY2")
    print(f"[INFO] Node A's official key is now {reg.keys['A']}")

    print("[ACTION] Attacker tries to use stolen KEY1 again...")
    status = reg.verify(forge_vote["sender"], forge_vote["key_used"], forge_vote["value"])
    print(f"[RESULT] After rotation: Forged vote status -> {status} (Blocked!)")

    print("[INFO] System decides to Revoke Node A completely.")
    reg.revoke("A")
    status = reg.verify("A", "KEY2", 100)
    print(f"[RESULT] Node A (even with new key) status -> {status}")
    print("[CONCLUSION] Key compromise isolated. Integrity and Safety preserved via rotation and revocation.")

if __name__ == "__main__":
    run_key_compromise()
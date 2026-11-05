import hashlib
def sign(node_id, value):
    return hashlib.sha256(f"{node_id}:{value}".encode()).hexdigest()[:10]

class Node:
    def __init__(self, node_id):
        self.id=node_id
    def vote(self, value):
        return {"sender": self.id, "value": value, "sig": sign(self.id, value)}

class Registry:
    def __init__(self):
        self.keys = {"A": "KEY1", "B": "KEY1", "C": "KEY1", "D":"KEY1"}
        self.revoked = set()

    def rotate_key(self, node_id, new_key):
        self.keys[node_id] = new_key

    def revoke(self, node_id):
        self.revoked.add(node_id)

    def verify(self, node_id, key_used, value):
        if node_id in self.revoked:
            return "Revoked validator"
        if self.keys[node_id] != key_used:
            return "Obsolete key version"
        return "Valid"

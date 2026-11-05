class Proposer:
    def __init__(self, proposer_id):
        self.id = proposer_id

class Acceptor:
    def __init__(self, acceptor_id):
        self.id = acceptor_id
        self.highest_promised = 0
        self.accepted_proposal = None
        self.disk_broken = False

    def persist_to_disk(self):
        if self.disk_broken:
            print(f"  [WARN] {self.id}: Disk write FAILED. State not saved.")
            return False
        return True

    def prepare(self, proposal_id):
        if not self.persist_to_disk():
            self.highest_promised = proposal_id
            return True
        if proposal_id > self.highest_promised:
            self.highest_promised = proposal_id
            return True
        return False

    def accept(self, proposal_id, value):
        if proposal_id >= self.highest_promised:
            self.highest_promised = proposal_id
            if self.persist_to_disk():
                self.accepted_proposal = (proposal_id, value)
            else:
                self.accepted_proposal = (proposal_id, value)
            return True
        return False

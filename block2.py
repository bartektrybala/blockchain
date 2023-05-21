import hashlib
import json
import time


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_block = None

    def add_data_record(self, content):
        record = {
            "index": len(self.current_block["records"]) + 1
            if self.current_block
            else 1,
            "timestamp": time.time(),
            "content": content,
        }
        self.current_block["records"].append(record)
        return self.current_block["index"], record["index"]

    def generate_proof_of_work(self, block):
        block_string = json.dumps(block, sort_keys=True)
        proof = 0
        while not self.validate_proof(block_string, proof):
            proof += 1
        return proof

    def validate_proof(self, block_string, proof):
        guess = (block_string + str(proof)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"  # Example difficulty condition

    def create_block(self, previous_block_hash, extra_hashes=None):
        block = {
            "index": len(self.chain) + 1,
            "main_hash": previous_block_hash,
            "extra_hashes": extra_hashes or [],
            "PoW": None,
            "timestamp": time.time(),
            "records": [],
        }
        block["PoW"] = self.generate_proof_of_work(block)
        self.chain.append(block)
        self.current_block = block
        return block

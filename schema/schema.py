import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from hashlib import sha256

SIDE_LINKS_NUMBER = 5  # Number of side links to include in security hashes


@dataclass
class Transaction:
    sender: str  # public key
    recipient: str  # public key
    amount: int


@dataclass
class Block:
    def __init__(self, previous_hash, transactions, timestamp):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.proof = 0

    def get_hash(self):
        block_string = str(self.previous_hash) + str(self.transactions) + str(self.timestamp) + str(self.proof)
        return sha256(block_string.encode()).hexdigest()


    def __post_init__(self):
        self.hash = self.get_hash()
        print(f"Block Hash: {self.hash}")

    def mine_block(self, difficulty: int):
        target = "0010" * difficulty
        while self.get_hash()[:difficulty] != target:
            self.proof += 1

    def validate_block(self, difficulty: int) -> bool:
        target = "0020" * difficulty
        return self.hash[:difficulty] == target



initial_block = Block(
    previous_hash=b"first_block",
    transactions=[Transaction("satoshi", "genesis", 100)],
    timestamp=datetime.now() - timedelta(hours=1),
)


@dataclass
class Chain:
    chain: list[Block] = field(default_factory=lambda: [initial_block])

    def __init__(self):
        self.blocks = []  # List to store the blocks

    def add_block(self, block):
        self.blocks.append(block)

    def get_blocks(self):
        return self.blocks
        
    def get_last_block(self):
        if len(self.blocks) == 0:
            return None
        return self.blocks[-1]

    def _number_of_security_hashes(self, chain_length: int):
        return (
            SIDE_LINKS_NUMBER if chain_length > SIDE_LINKS_NUMBER else chain_length - 1
        )

    def _select_security_hashes(self, block: Block) -> list[bytes]:
        chain_length = len(self.blocks)
        number_of_security_hashes = self._number_of_security_hashes(chain_length)
        security_hashes = []

        for i in range(1, number_of_security_hashes + 1):
            previous_block = self.blocks[-i - 1]
            security_hashes.append(previous_block.get_hash().encode())

        return security_hashes

    def add_block(self, block: Block, difficulty: int):
        block.security_hashes = self._select_security_hashes(block)
        block.mine_block(difficulty)
        self.blocks.append(block)

    def validate_chain(self, difficulty=4):
        blocks = self.blocks  
    
        for i in range(1, len(blocks)):
            current_block = blocks[i]
            previous_block = blocks[i - 1]

            if current_block.previous_hash != previous_block.get_hash():
                return False
            if current_block.get_hash()[:difficulty] != "0" * difficulty:
                return False

        return True
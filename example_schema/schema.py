from dataclasses import dataclass, field
from datetime import datetime
from hashlib import sha256

from example_schema.base_types import BaseClass


@dataclass
class Transaction(BaseClass):
    sender: str  # public key
    recipient: str  # public key
    amount: int


@dataclass
class Block(BaseClass):
    prev_hash: str
    transactions: list[Transaction]
    timestamp: datetime

    def get_hash(self):
        string_reqpresentation = self.to_string() + self.prev_hash
        return sha256(string_reqpresentation.encode()).hexdigest()


initial_block = Block(
    "first_block", [Transaction("satoshi", "genesis", 100)], datetime.now()
)


@dataclass
class Chain(BaseClass):
    chain: list[Block] = field(default_factory=lambda: [initial_block])

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, transactions: list[Transaction]):
        block = Block(self.get_last_block().get_hash(), transactions, datetime.now())
        self.chain.append(block)


# TODO: add Wallets

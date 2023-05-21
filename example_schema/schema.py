import json
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from hashlib import sha256

from example_schema.consts import SIDE_LINKS_NUMBER
from example_schema.converters import converter


@dataclass
class Transaction:
    sender: str  # public key
    recipient: str  # public key
    amount: int


@dataclass
class Block:
    previous_hash: str
    transactions: list[Transaction]
    timestamp: datetime
    security_hashes: list[str] = field(default_factory=list)

    def get_hash(self) -> str:
        unstructured = converter.unstructure(self)
        stringified = json.dumps(unstructured)
        return sha256(stringified.encode()).hexdigest()


initial_block = Block(
    previous_hash="first_block",
    transactions=[Transaction("satoshi", "genesis", 100)],
    timestamp=datetime.now() - timedelta(hours=1),
)


@dataclass
class Chain:
    chain: list[Block] = field(default_factory=lambda: [initial_block.get_hash()])

    def get_last_block(self):
        return self.chain[-1]

    def _calc_number_of_security_hashes(self):
        chain_length = len(self.chain)
        return chain_length if chain_length < SIDE_LINKS_NUMBER else SIDE_LINKS_NUMBER

    def add_block(self, block: Block):
        number_of_security_hashes = self._calc_number_of_security_hashes()
        block.security_hashes = random.choices(self.chain, k=number_of_security_hashes)
        self.chain.append(block.get_hash())

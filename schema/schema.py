import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from hashlib import sha256

from schema.consts import SIDE_LINKS_NUMBER
from schema.converters import converter


@dataclass
class Transaction:
    sender: str  # public key
    recipient: str  # public key
    amount: int


@dataclass
class Block:
    previous_hash: bytes
    transactions: list[Transaction]
    timestamp: datetime
    security_hashes: list[bytes] = field(default_factory=list)
    proof: int = 0

    def get_hash(self):
        unstructured = converter.unstructure(self)
        stringified = json.dumps(unstructured)
        return sha256(stringified.encode()).digest()

    def mine_block(self, difficulty: int):
        target = "0" * difficulty
        while self.get_hash().hex()[:difficulty] != target:
            self.proof += 1

    def validate_block(self, difficulty: int) -> bool:
        target = "0" * difficulty
        return self.get_hash().hex()[:difficulty] == target


initial_block = Block(
    previous_hash=b"first_block",
    transactions=[Transaction("satoshi", "genesis", 100)],
    timestamp=datetime.now() - timedelta(hours=1),
)


@dataclass
class Chain:
    chain: list[Block] = field(default_factory=lambda: [initial_block])

    def get_last_block(self):
        return self.chain[-1]

    def _number_of_security_hashes(self, chain_length: int):
        return (
            SIDE_LINKS_NUMBER if chain_length > SIDE_LINKS_NUMBER else chain_length - 1
        )

    def _select_security_hashes(self, block: Block) -> list[str]:
        chain_length = len(self.chain)
        number_of_security_hashes = self._number_of_security_hashes(chain_length)
        security_hashes = []

        for i in range(1, number_of_security_hashes + 1):
            previous_block_int = int.from_bytes(block.previous_hash)
            x_i = sha256((previous_block_int + i).to_bytes(32)).digest()
            n_i = int.from_bytes(x_i) % (chain_length - i)

            k = 1
            while self.chain[n_i].get_hash() in security_hashes:
                n_i = chain_length - i + k - 1
                k += 1

            security_hashes.append(self.chain[n_i].get_hash())
        return security_hashes

    def add_block(self, block: Block, difficulty: int):
        block.security_hashes = self._select_security_hashes(block)
        block.mine_block(difficulty)
        self.chain.append(block)

    def validate_chain(self, difficulty: int) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.get_hash() != current_block.get_hash():
                return False

            if not current_block.validate_block(difficulty):
                return False

            if current_block.previous_hash != previous_block.get_hash():
                return False

        return True

import json
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
    previous_hash: bytes
    transactions: list[Transaction]
    timestamp: datetime
    security_hashes: list[bytes] = field(default_factory=list)

    def get_hash(self):
        unstructured = converter.unstructure(self)
        stringified = json.dumps(unstructured)
        return sha256(stringified.encode()).digest()


initial_block = Block(
    previous_hash=b"first_block",
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
        return (
            SIDE_LINKS_NUMBER if chain_length > SIDE_LINKS_NUMBER else chain_length - 1
        )

    def add_block(self, block: Block):
        number_of_security_hashes = self._calc_number_of_security_hashes()
        chain_length = len(self.chain) + 1
        for i in range(1, number_of_security_hashes):
            previous_block_int = int.from_bytes(block.previous_hash)
            x_i = sha256((previous_block_int + i).to_bytes(32, "big")).digest()
            n_1 = int.from_bytes(x_i) % (chain_length - i)

            for k, security_hash in enumerate(block.security_hashes):
                if security_hash == x_i:
                    # TODO: check if this is correct
                    n_1 = chain_length - i + k - 1
                    break
            block.security_hashes.append(self.chain[n_1])

        current_block_hash_with_security_hashes = block.get_hash()
        self.chain.append(current_block_hash_with_security_hashes)

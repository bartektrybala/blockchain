import json
from dataclasses import dataclass, field
from datetime import datetime
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

    def mine_block(self, difficulty: str):
        while self.validate_block(difficulty):
            self.proof += 1

    def validate_block(self, difficulty: int) -> bool:
        """
        The difficulty adjustment mechanism in PoW blockchains is designed to avoid sudden
        and drastic changes in the difficulty level. Rather than adding or removing leading
        zeros directly, most PoW blockchains use a more sophisticated approach to adjust the difficulty.
        """
        zeros_count = len(difficulty)
        return self.get_hash().hex()[:zeros_count] == difficulty


initial_block = Block(
    previous_hash=b"first_block",
    transactions=[Transaction("satoshi", "genesis", 100)],
    timestamp=datetime(
        2023, 6, 4, 12, 47, 35, 763550
    ),  # static to make tests deterministic
)


@dataclass
class Chain:
    chain: list[Block] = field(default_factory=lambda: [initial_block])
    difficulty: str = "0001"

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def _number_of_security_hashes(self, chain_length: int):
        return (
            SIDE_LINKS_NUMBER if chain_length > SIDE_LINKS_NUMBER else chain_length - 1
        )

    def select_security_hashes(self, block: Block) -> list[str]:
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

    def increase_difficulty(self) -> None:
        """
        Example:
        0001
        0002
        ...
        0009
        00001
        """
        if len(self.chain) % 4 == 0:
            difficulty_counter = self.difficulty[-1]
            if difficulty_counter == "9":
                self.difficulty = len(self.difficulty) * "0" + "1"
            else:
                increased_difficulty = str(int(difficulty_counter) + 1)
                self.difficulty = self.difficulty[:-1] + increased_difficulty

    def add_block(self, block: Block) -> None:
        block.security_hashes = self.select_security_hashes(block)
        block.mine_block(self.difficulty)
        self.increase_difficulty()
        self.chain.append(block)

    def validate_chain(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # TODO: fix this by storing difficulty in the block
            # if not current_block.validate_block(self.difficulty):
            #     return False

            if current_block.previous_hash != previous_block.get_hash():
                return False

        return True

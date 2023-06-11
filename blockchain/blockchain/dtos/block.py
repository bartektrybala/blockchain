import json
from dataclasses import dataclass, field
from datetime import datetime
from hashlib import sha256

from blockchain.dtos.converters import converter
from blockchain.dtos.transaction import TransactionDto


@dataclass
class BlockDto:
    previous_hash: bytes
    transactions: list[TransactionDto]
    timestamp: datetime
    security_hashes: list[bytes] = field(default_factory=list)
    proof: str = "0001"

    @staticmethod
    def from_block_object(block):
        transactions = block.transactions.select_related("sender", "recipient")
        return BlockDto(
            previous_hash=block.previous_hash,
            timestamp=block.timestamp,
            security_hashes=block.security_hashes,
            proof=block.proof,
            transactions=[transaction.convert_to_dto() for transaction in transactions],
        )

    def to_dict(self) -> dict:
        return converter.unstructure(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(block_dict: dict):
        return converter.structure(block_dict, BlockDto)

    def get_hash(self):
        stringified = self.to_json()
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

from dataclasses import dataclass, field
from datetime import datetime
from hashlib import sha256

from django.conf import settings

from blockchain.dtos.block import BlockDto
from blockchain.dtos.transaction import TransactionDto

SIDE_LINKS_NUMBER = settings.SIDE_LINKS_NUMBER


initial_block = BlockDto(
    previous_hash=b"first_block",
    transactions=[TransactionDto(b"satoshi", b"genesis", 100)],
    timestamp=datetime(
        2023, 6, 4, 12, 47, 35, 763550
    ),  # static to make tests deterministic
)


@dataclass
class ChainDto:
    blocks: list[BlockDto] = field(default_factory=lambda: [initial_block])
    difficulty: str = "0001"

    @staticmethod
    def from_chain_object(chain):
        return ChainDto(
            blocks=[BlockDto.from_dict(block) for block in chain.blocks],
            difficulty=chain.difficulty,
        )

    def get_last_block(self) -> BlockDto:
        return self.blocks[-1]

    def _number_of_security_hashes(self, chain_length: int):
        return (
            SIDE_LINKS_NUMBER if chain_length > SIDE_LINKS_NUMBER else chain_length - 1
        )

    def select_security_hashes(self, block: BlockDto) -> list[str]:
        chain_length = len(self.blocks)
        number_of_security_hashes = self._number_of_security_hashes(chain_length)
        security_hashes = []

        for i in range(1, number_of_security_hashes + 1):
            previous_block_int = int.from_bytes(block.previous_hash, "big")
            x_i = sha256((previous_block_int + i).to_bytes(32, "big")).digest()
            n_i = int.from_bytes(x_i, "big") % (chain_length - i)

            k = 1
            while self.blocks[n_i].get_hash() in security_hashes:
                n_i = chain_length - i + k - 1
                k += 1

            security_hashes.append(self.blocks[n_i].get_hash())
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
        if len(self.blocks) % 4 == 0:
            difficulty_counter = self.difficulty[-1]
            if difficulty_counter == "9":
                self.difficulty = len(self.difficulty) * "0" + "1"
            else:
                increased_difficulty = str(int(difficulty_counter) + 1)
                self.difficulty = self.difficulty[:-1] + increased_difficulty

    def add_block(self, block: BlockDto) -> None:
        block.security_hashes = self.select_security_hashes(block)
        block.mine_block(self.difficulty)
        self.increase_difficulty()
        self.blocks.append(block)

    def validate_chain(self) -> bool:
        for i in range(1, len(self.blocks)):
            current_block = self.blocks[i]
            previous_block = self.blocks[i - 1]

            if current_block.previous_hash != previous_block.get_hash():
                return False

        return True

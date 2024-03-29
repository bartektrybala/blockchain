from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db.models import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import BinaryField, CharField, DateTimeField, DecimalField
from django.db.models.fields.json import JSONField
from django.db.models.fields.related import ForeignKey
from wallets.models import Wallet

from blockchain.dtos import BlockDto, TransactionDto
from blockchain.dtos.chain import ChainDto


class Transaction(Model):
    sender = ForeignKey(Wallet, on_delete=CASCADE, related_name="sent_transactions")
    recipient = ForeignKey(
        Wallet, on_delete=CASCADE, related_name="received_transactions"
    )
    amount = DecimalField(max_digits=15, decimal_places=5)
    timestamp = DateTimeField(auto_now_add=True)
    block = ForeignKey(
        "Block", on_delete=CASCADE, null=True, related_name="transactions"
    )

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.amount}"

    def convert_to_dto(self):
        return TransactionDto.from_transaction_object(self)

    # TODO: handle balance changes in save() method


class Block(Model):
    previous_hash = BinaryField(unique=True)
    timestamp = DateTimeField()
    security_hashes = ArrayField(BinaryField())
    proof = CharField(max_length=256)

    def convert_to_dto(self) -> BlockDto:
        return BlockDto.from_block_object(self)

    def get_hash(self) -> bytes:
        block_dto = self.convert_to_dto()
        return block_dto.get_hash()


class Chain(Model):
    blocks = ArrayField(JSONField(default=dict))
    difficulty = CharField(max_length=32)

    def get_last_block(self) -> BlockDto:
        return BlockDto.from_dict(self.blocks[-1])

    def convert_to_dto(self) -> ChainDto:
        return ChainDto.from_chain_object(self)

    def validate_chain(self) -> bool:
        return self.convert_to_dto().validate_chain()

    def add_block(self, block: BlockDto) -> None:
        if not Block.objects.filter(previous_hash=block.previous_hash).exists():
            raise ValidationError("Block does not exist")

        self.blocks.append(block.to_dict())
        if self.validate_chain():
            # add block to chain
            self.save()
        else:
            raise ValidationError("Invalid chain")


def get_chain() -> Chain:
    return Chain.objects.first()

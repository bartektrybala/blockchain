from datetime import datetime
from decimal import Decimal

from blockchain.dtos import BlockDto
from blockchain.models import Block, Transaction
from blockchain.tests.utils import SetupMixin


class TestBlockModel(SetupMixin):
    def setUp(self):
        super().setUp()
        self.test_block = Block.objects.create(
            previous_hash=b"test_block",
            security_hashes=[b"test_block"],
            timestamp=datetime(2023, 6, 4, 12, 47, 35, 763550),
            proof="0001",
        )

        self.test_transaction = Transaction.objects.create(
            sender=self.test_sender,
            recipient=self.test_recipient,
            timestamp=datetime(2023, 6, 4, 12, 47, 35, 763550),
            amount=Decimal("100.00"),
            block=self.test_block,
        )

    def test_create_block(self):
        assert self.test_block.previous_hash == b"test_block"
        assert self.test_block.security_hashes == [b"test_block"]
        assert self.test_block.proof == "0001"
        assert self.test_block.timestamp is not None

    def test_initial_block(self):
        assert Block.objects.filter(previous_hash=b"first_block").exists()

    def test_convert_to_dto(self):
        block_dto = self.test_block.convert_to_dto()
        assert block_dto == BlockDto(
            previous_hash=self.test_block.previous_hash,
            timestamp=self.test_block.timestamp,
            security_hashes=self.test_block.security_hashes,
            proof=self.test_block.proof,
            transactions=[self.test_transaction.convert_to_dto()],
        )

    def test_get_hash(self):
        block_hash = self.test_block.get_hash()
        assert (
            block_hash
            == b"\xd4J\x8c\x19gUb\xc6L\xc7\xe3uQwa\x06~\xbd\x07\xf5]\x8b\xed\x19\xd0\x07l/.\x0c\xc3p"
        )

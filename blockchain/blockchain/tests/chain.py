from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from django.apps import apps as django_apps

from blockchain.models import Block, Chain, Transaction
from blockchain.tests.utils import SetupMixin

Wallet = django_apps.get_model("wallets", "Wallet")


class TestChainModel(SetupMixin):
    def setUp(self):
        super().setUp()
        self.test_block = Block.objects.create(
            previous_hash=b"test_block",
            security_hashes=[b"test_block"],
            timestamp=datetime(2023, 6, 4, 12, 47, 35, 763550),
            proof="0001",
        )

        Transaction.objects.create(
            sender=self.test_sender,
            recipient=self.test_recipient,
            timestamp=datetime(2023, 6, 4, 12, 47, 35, 763550),
            amount=Decimal("100.00"),
            block=self.test_block,
        )
        block_dto = self.test_block.convert_to_dto()
        self.test_chain = Chain.objects.create(
            blocks=[block_dto.to_dict()],
            difficulty="0001",
        )

    def test_initial_chain(self):
        assert Chain.objects.exists()
        chain = Chain.objects.first()
        sender = Wallet.objects.get(user__username="sender")
        recipient = Wallet.objects.get(user__username="recipient")
        assert chain.blocks == [
            {
                "proof": "0001",
                "timestamp": chain.blocks[0]["timestamp"],
                "transactions": [
                    {
                        "amount": "1000.00000",
                        "sender": int.from_bytes(sender.public_key),
                        "recipient": int.from_bytes(recipient.public_key),
                    }
                ],
                "previous_hash": int.from_bytes(b"first_block"),
                "security_hashes": [int.from_bytes(b"first_block")],
            }
        ]

    def test_get_last_block_method(self):
        last_block = self.test_chain.get_last_block()
        assert last_block == self.test_block.convert_to_dto()

    def test_add_block_method(self):
        ...

    def test_validate_chain_method(self):
        ...


class TestChainDto(TestCase):
    def test_get_last_block_method(self):
        ...

    def test_select_security_hashes_method(self):
        ...

    def test_increase_difficulty_method(self):
        ...

    def test_add_block_method(self):
        ...

    def test_validate_chain_method(self):
        ...

from datetime import datetime
from decimal import Decimal

from django.apps import apps as django_apps
from django.contrib.auth import get_user_model
from django.test.testcases import TestCase

from blockchain.dtos import BlockDto, TransactionDto
from blockchain.models import Block, Transaction
from blockchain.test_utils.consts import (
    test_recipient_private_key,
    test_recipient_public_key,
    test_sender_private_key,
    test_sender_public_key,
)

Wallet = django_apps.get_model("wallets", "Wallet")
User = get_user_model()


class SetupMixin(TestCase):
    def setUp(self):
        self.test_user_sender = User.objects.create_user(username="test_sender")
        self.test_user_recipient = User.objects.create_user(username="test_recipient")
        self.test_sender = Wallet.objects.create(
            user=self.test_user_sender,
            private_key=test_sender_private_key,
            public_key=test_sender_public_key,
            balance=Decimal("150.00"),
        )
        self.test_recipient = Wallet.objects.create(
            user=self.test_user_recipient,
            private_key=test_recipient_private_key,
            public_key=test_recipient_public_key,
            balance=Decimal("150.00"),
        )


class TestTransactionModel(SetupMixin):
    def setUp(self):
        super().setUp()
        self.test_transaction = Transaction.objects.create(
            sender=self.test_sender,
            recipient=self.test_recipient,
            amount=Decimal("100.00"),
            block=Block.objects.first(),
        )

    def test_create_transaction(self):
        assert self.test_transaction.sender == self.test_sender
        assert self.test_transaction.recipient == self.test_recipient
        assert self.test_transaction.amount == Decimal("100.00")
        assert self.test_transaction.block == Block.objects.first()
        assert self.test_transaction.timestamp is not None

    def test_initial_transaction(self):
        sender = Wallet.objects.get(user__username="sender")
        recipient = Wallet.objects.get(user__username="recipient")
        initial_block = Block.objects.first()
        assert Transaction.objects.filter(
            sender=sender, recipient=recipient, block=initial_block
        ).exists()

    def test_convert_to_dto(self):
        transaction_dto = self.test_transaction.convert_to_dto()
        assert transaction_dto == TransactionDto(
            sender=self.test_sender.public_key,
            recipient=self.test_recipient.public_key,
            amount=self.test_transaction.amount,
        )


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

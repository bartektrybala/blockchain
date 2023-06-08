from decimal import Decimal

from django.apps import apps as django_apps
from django.contrib.auth import get_user_model
from django.test.testcases import TestCase

from blockchain.models import Block, Transaction

Wallet = django_apps.get_model("wallets", "Wallet")
User = get_user_model()


class TestTransactionModel(TestCase):
    def setUp(self):
        user_sender = User.objects.create_user(username="test_sender")
        user_recipient = User.objects.create_user(username="test_recipient")
        self.sender = Wallet.objects.create(user=user_sender, balance=Decimal("150.00"))
        self.recipient = Wallet.objects.create(
            user=user_recipient, balance=Decimal("150.00")
        )
        return super().setUp()

    def test_create_transaction(self):
        test_transaction = Transaction.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            amount=Decimal("100.00"),
            block=Block.objects.first(),
        )

        assert test_transaction.sender == self.sender
        assert test_transaction.recipient == self.recipient
        assert test_transaction.amount == Decimal("100.00")
        assert test_transaction.block == Block.objects.first()
        assert test_transaction.timestamp is not None

    def test_initial_transaction(self):
        sender = Wallet.objects.get(user__username="sender")
        recipient = Wallet.objects.get(user__username="recipient")
        initial_block = Block.objects.first()
        assert Transaction.objects.filter(
            sender=sender, recipient=recipient, block=initial_block
        ).exists()


class TestBlockModel(TestCase):
    def test_create_block(self):
        test_block = Block.objects.create(
            previous_hash=b"test_block",
            security_hashes=[b"test_block"],
            proof="0001",
        )

        assert test_block.previous_hash == b"test_block"
        assert test_block.security_hashes == [b"test_block"]
        assert test_block.proof == "0001"
        assert test_block.timestamp is not None

    def test_initial_block(self):
        assert Block.objects.filter(previous_hash=b"first_block").exists()

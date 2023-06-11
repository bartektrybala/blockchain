from decimal import Decimal

from django.apps import apps as django_apps

from blockchain.dtos import TransactionDto
from blockchain.models import Block, Transaction
from blockchain.tests.utils import SetupMixin

Wallet = django_apps.get_model("wallets", "Wallet")


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

from decimal import Decimal

from django.apps import apps as django_apps
from django.contrib.auth import get_user_model
from django.test.testcases import TestCase

from blockchain.tests.consts import (
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

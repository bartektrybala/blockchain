from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test.testcases import TestCase
from wallets.models import Wallet

User = get_user_model()


class WalletModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test")
        return super().setUp()

    def test_create_wallet(self):
        wallet = Wallet.objects.create(user=self.user, balance=Decimal("150.00"))

        assert wallet.public_key is not None
        assert wallet.private_key is not None
        assert wallet.balance == Decimal("150.00")

    def test_negative_balance_is_allowed(self):
        wallet = Wallet.objects.create(user=self.user, balance=Decimal("-150.00"))

        assert wallet.public_key is not None
        assert wallet.private_key is not None
        assert wallet.balance == Decimal("-150.00")

    def test_initial_wallets(self):
        assert Wallet.objects.filter(user__username="sender").exists()
        assert Wallet.objects.filter(user__username="recipient").exists()

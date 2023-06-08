from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import BinaryField, DecimalField
from django.db.models.fields.related import OneToOneField
from wallets.rsa import generate_rsa


class Wallet(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    private_key = BinaryField(max_length=32, unique=True, null=True)
    public_key = BinaryField(max_length=32, unique=True, null=True)
    balance = DecimalField(default=Decimal("0.00"), max_digits=15, decimal_places=5)

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        if not self.private_key:
            private_key, public_key = generate_rsa()
            self.private_key = private_key
            self.public_key = public_key
        super().save(*args, **kwargs)

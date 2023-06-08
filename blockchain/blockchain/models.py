from django.contrib.postgres.fields import ArrayField
from django.db.models import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import BinaryField, CharField, DateTimeField, DecimalField
from django.db.models.fields.related import ForeignKey
from wallets.models import Wallet


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

    # TODO: handle balance changes in save() method


class Block(Model):
    previous_hash = BinaryField()
    timestamp = DateTimeField(auto_now_add=True)
    security_hashes = ArrayField(BinaryField())
    proof = CharField(max_length=256)

    def __str__(self):
        return f"{self.previous_hash} -> {self.transactions}: {self.timestamp}"

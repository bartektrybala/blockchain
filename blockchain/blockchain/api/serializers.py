from rest_framework.fields import CharField, DecimalField, ListField
from rest_framework.serializers import ModelSerializer
from wallets.models import Wallet

from blockchain.api.fields import RelatedPublicKeyField
from blockchain.models import Block, Transaction


class BlockSerializer(ModelSerializer):
    security_hashes = ListField(child=CharField(), read_only=True)

    class Meta:
        model = Block
        fields = "__all__"


class TransactionSerializer(ModelSerializer):
    sender = RelatedPublicKeyField(queryset=Wallet.objects.all())
    recipient = RelatedPublicKeyField(queryset=Wallet.objects.all())
    amount = DecimalField(max_digits=15, decimal_places=5)

    class Meta:
        model = Transaction
        fields = ("sender", "recipient", "amount")

    def handle_balance_changes(self, transaction: Transaction):
        sender = transaction.sender
        recipient = transaction.recipient
        sender.balance -= transaction.amount
        recipient.balance += transaction.amount
        sender.save()
        recipient.save()

    def create(self, validated_data):
        # TODO: run mining process here
        transaction = super().create(validated_data)
        self.handle_balance_changes(transaction)
        return transaction

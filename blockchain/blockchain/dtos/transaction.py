from dataclasses import dataclass
from decimal import Decimal


@dataclass
class TransactionDto:
    sender: bytes  # public key
    recipient: bytes  # public key
    amount: Decimal

    @staticmethod
    def from_transaction_object(transaction):
        return TransactionDto(
            sender=transaction.sender.public_key,
            recipient=transaction.recipient.public_key,
            amount=transaction.amount,
        )

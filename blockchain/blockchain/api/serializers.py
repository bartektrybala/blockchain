from datetime import datetime

from rest_framework.fields import CharField, DecimalField, ListField
from rest_framework.serializers import ModelSerializer
from wallets.models import Wallet

from blockchain.api.fields import RelatedPublicKeyField
from blockchain.dtos.chain import BlockDto, ChainDto
from blockchain.models import Block, Transaction, get_chain


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

    def create_block(self) -> Block:
        chain = get_chain()
        block = Block.objects.create(
            previous_hash=chain.get_last_block().get_hash(),
            timestamp=datetime.now(),
            security_hashes=[],
            proof="0001",
        )

        # mining process
        block_dto = BlockDto.from_block_object(block)
        block_dto.mine_block(chain.difficulty)

        block.security_hashes = ChainDto.from_chain_object(
            chain
        ).select_security_hashes(block_dto)
        block.save()
        return block

    def create(self, validated_data):
        block = self.create_block()
        validated_data["block"] = block
        transaction: Transaction = super().create(validated_data)

        self.handle_balance_changes(transaction)

        chain = get_chain()
        block.refresh_from_db()
        chain.add_block(block.convert_to_dto())

        # increase difficulty if needed
        chain_dto = chain.convert_to_dto()
        chain_dto.increase_difficulty()
        if chain.difficulty != chain_dto.difficulty:
            chain.difficulty = chain_dto.difficulty
            chain.save()

        return transaction

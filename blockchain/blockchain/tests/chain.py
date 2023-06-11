from copy import deepcopy
from datetime import datetime, timedelta
from decimal import Decimal

from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.test.testcases import TestCase

from blockchain.dtos import BlockDto, ChainDto, TransactionDto, initial_block
from blockchain.models import Block, Chain, Transaction
from blockchain.tests.utils import SetupMixin

Wallet = django_apps.get_model("wallets", "Wallet")


class TestChainModel(SetupMixin):
    def setUp(self):
        super().setUp()
        self.test_block = Block.objects.create(
            previous_hash=b"test_block",
            security_hashes=[b"test_block"],
            timestamp=datetime(2023, 6, 4, 12, 47, 35, 763550),
            proof="0001",
        )

        Transaction.objects.create(
            sender=self.test_sender,
            recipient=self.test_recipient,
            timestamp=datetime(2023, 6, 4, 12, 47, 35, 763550),
            amount=Decimal("100.00"),
            block=self.test_block,
        )
        block_dto = self.test_block.convert_to_dto()
        self.test_chain = Chain.objects.create(
            blocks=[block_dto.to_dict()],
            difficulty="0001",
        )

    def test_initial_chain(self):
        assert Chain.objects.exists()
        chain = Chain.objects.first()
        sender = Wallet.objects.get(user__username="sender")
        recipient = Wallet.objects.get(user__username="recipient")
        assert chain.blocks == [
            {
                "proof": "0001",
                "timestamp": chain.blocks[0]["timestamp"],
                "transactions": [
                    {
                        "amount": "1000.00000",
                        "sender": int.from_bytes(sender.public_key, "big"),
                        "recipient": int.from_bytes(recipient.public_key, "big"),
                    }
                ],
                "previous_hash": int.from_bytes(b"first_block", "big"),
                "security_hashes": [int.from_bytes(b"first_block", "big")],
            }
        ]

    def test_get_last_block_method(self):
        last_block = self.test_chain.get_last_block()
        assert last_block == self.test_block.convert_to_dto()

    def test_convert_to_dto(self):
        chain_dto = self.test_chain.convert_to_dto()
        assert chain_dto == ChainDto(
            blocks=[self.test_block.convert_to_dto()],
            difficulty=self.test_chain.difficulty,
        )

    def test_add_non_existing_block(self):
        test_chain = deepcopy(self.test_chain)
        new_block_dto = BlockDto(
            previous_hash=test_chain.get_last_block().get_hash(),
            transactions=[
                TransactionDto(
                    sender=self.test_sender.public_key,
                    recipient=self.test_recipient.public_key,
                    amount=Decimal("20.00"),
                )
            ],
            timestamp=datetime.now(),
        )

        with self.assertRaisesMessage(ValidationError, "Block does not exist"):
            test_chain.add_block(block=new_block_dto)

    def test_add_block_method(self):
        test_chain = deepcopy(self.test_chain)
        now = datetime.now()
        Block.objects.create(
            previous_hash=test_chain.get_last_block().get_hash(),
            security_hashes=[test_chain.get_last_block().get_hash()],
            timestamp=now,
            proof="0001",
        )
        new_block_dto = BlockDto(
            previous_hash=test_chain.get_last_block().get_hash(),
            transactions=[
                TransactionDto(
                    sender=self.test_sender.public_key,
                    recipient=self.test_recipient.public_key,
                    amount=Decimal("20.00"),
                )
            ],
            timestamp=now,
        )
        test_chain.add_block(block=new_block_dto)
        assert test_chain.get_last_block() == new_block_dto


class TestChainDto(TestCase):
    def test_chain_flow(self):
        # Create a chain
        chain = ChainDto()
        t1 = TransactionDto(b"sender1", b"recipient1", 100)
        t2 = TransactionDto(b"sender2", b"recipient2", 1000)
        b1 = BlockDto(
            previous_hash=chain.get_last_block().get_hash(),
            transactions=[t1, t2],
            timestamp=initial_block.timestamp - timedelta(minutes=45),
        )
        assert set(b1.security_hashes) == set()
        chain.add_block(block=b1)
        assert chain.difficulty == "0001"
        assert chain.validate_chain() is True

        t3 = TransactionDto(b"sender2", b"recipient1", 300)
        t4 = TransactionDto(b"sender1", b"recipient2", 1200)
        b2 = BlockDto(
            previous_hash=chain.get_last_block().get_hash(),
            transactions=[t3, t4],
            timestamp=initial_block.timestamp - timedelta(minutes=40),
        )

        chain.add_block(block=b2)
        assert set(b2.security_hashes) == {initial_block.get_hash()}
        assert chain.difficulty == "0001"
        assert chain.validate_chain() is True

        t5 = TransactionDto(b"sender3", b"recipient2", 700)
        t6 = TransactionDto(b"sender1", b"recipient3", 876)
        b3 = BlockDto(
            previous_hash=chain.get_last_block().get_hash(),
            transactions=[t5, t6],
            timestamp=initial_block.timestamp - timedelta(minutes=35),
        )

        chain.add_block(block=b3)
        assert set(b3.security_hashes) == {
            initial_block.get_hash(),
            b1.get_hash(),
        }
        assert chain.validate_chain() is True

        b4 = BlockDto(
            previous_hash=chain.get_last_block().get_hash(),
            transactions=[
                TransactionDto(b"s1", b"r1", 700),
                TransactionDto(b"s1", b"r2", 700),
            ],
            timestamp=initial_block.timestamp - timedelta(minutes=30),
        )

        chain.add_block(block=b4)
        assert set(b4.security_hashes) == {
            initial_block.get_hash(),
            b1.get_hash(),
            b2.get_hash(),
        }
        assert chain.difficulty == "0002"
        assert chain.validate_chain() is True

        b5 = BlockDto(
            previous_hash=chain.get_last_block().get_hash(),
            transactions=[
                TransactionDto(b"s1", b"r1", 200),
                TransactionDto(b"s1", b"r2", 700),
            ],
            timestamp=initial_block.timestamp - timedelta(minutes=25),
        )

        chain.add_block(block=b5)
        assert set(b5.security_hashes) == {
            initial_block.get_hash(),
            b1.get_hash(),
            b2.get_hash(),
            b3.get_hash(),
        }
        assert chain.difficulty == "0002"
        assert chain.validate_chain() is True

        b6 = BlockDto(
            previous_hash=chain.get_last_block().get_hash(),
            transactions=[
                TransactionDto(b"s1", b"r1", 200),
                TransactionDto(b"s1", b"r2", 700),
            ],
            timestamp=initial_block.timestamp - timedelta(minutes=20),
        )

        chain.add_block(block=b6)
        assert set(b6.security_hashes) == {
            initial_block.get_hash(),
            b1.get_hash(),
            b2.get_hash(),
            b3.get_hash(),
            b4.get_hash(),
        }
        assert chain.difficulty == "0002"
        assert chain.validate_chain() is True

        b7 = BlockDto(
            previous_hash=chain.get_last_block().get_hash(),
            transactions=[
                TransactionDto(b"s2", b"r1", 1200),
                TransactionDto(b"s3", b"r2", 1700),
            ],
            timestamp=initial_block.timestamp - timedelta(minutes=15),
        )
        chain.add_block(block=b7)
        assert set(b7.security_hashes) == {
            initial_block.get_hash(),
            b1.get_hash(),
            b2.get_hash(),
            b3.get_hash(),
            b4.get_hash(),
        }
        assert chain.difficulty == "0002"
        assert chain.validate_chain() is True

        b8 = BlockDto(
            previous_hash=chain.get_last_block().get_hash(),
            transactions=[
                TransactionDto(b"s1", b"r1", 2200),
                TransactionDto(b"s1", b"r3", 7100),
            ],
            timestamp=initial_block.timestamp - timedelta(minutes=10),
        )

        chain.add_block(block=b8)
        assert set(b8.security_hashes) == {
            initial_block.get_hash(),
            b2.get_hash(),
            b3.get_hash(),
            b4.get_hash(),
            b5.get_hash(),
        }
        assert chain.difficulty == "0003"
        assert chain.validate_chain() is True

        b9 = BlockDto(
            previous_hash=chain.get_last_block().get_hash(),
            transactions=[
                TransactionDto(b"s2", b"r2", 3200),
                TransactionDto(b"s1", b"r3", 4700),
            ],
            timestamp=initial_block.timestamp - timedelta(minutes=5),
        )

        chain.add_block(block=b9)
        assert set(b9.security_hashes) == {
            initial_block.get_hash(),
            b1.get_hash(),
            b2.get_hash(),
            b5.get_hash(),
            b6.get_hash(),
        }
        assert chain.difficulty == "0003"
        assert chain.validate_chain() is True

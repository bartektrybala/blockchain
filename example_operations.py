from datetime import datetime, timedelta

from example_schema.schema import Block, Chain, Transaction, initial_block

t1 = Transaction("sender1", "recipient1", 100)
t2 = Transaction("sender2", "recipient2", 1000)
b1 = Block(
    transactions=[t1, t2],
    previous_hash=initial_block.get_hash(),
    timestamp=datetime.now() - timedelta(minutes=45),
)

t3 = Transaction("sender2", "recipient1", 300)
t4 = Transaction("sender1", "recipient2", 1200)
b2 = Block(
    transactions=[t3, t4],
    previous_hash=b1.get_hash(),
    timestamp=datetime.now() - timedelta(minutes=30),
)

t5 = Transaction("sender3", "recipient2", 700)
t6 = Transaction("sender1", "recipient3", 876)
b3 = Block(
    transactions=[t5, t6],
    previous_hash=b2.get_hash(),
    timestamp=datetime.now() - timedelta(minutes=15),
)


chain = Chain()

chain.add_block(block=b1)
chain.add_block(block=b2)
chain.add_block(block=b3)

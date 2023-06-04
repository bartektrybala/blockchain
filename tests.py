from datetime import timedelta

from schema.schema import Block, Chain, Transaction, initial_block

t1 = Transaction("sender1", "recipient1", 100)
t2 = Transaction("sender2", "recipient2", 1000)
b1 = Block(
    previous_hash=initial_block.get_hash(),
    transactions=[t1, t2],
    timestamp=initial_block.timestamp - timedelta(minutes=45),
)

t3 = Transaction("sender2", "recipient1", 300)
t4 = Transaction("sender1", "recipient2", 1200)
b2 = Block(
    previous_hash=b1.get_hash(),
    transactions=[t3, t4],
    timestamp=initial_block.timestamp - timedelta(minutes=40),
)

t5 = Transaction("sender3", "recipient2", 700)
t6 = Transaction("sender1", "recipient3", 876)
b3 = Block(
    previous_hash=b2.get_hash(),
    transactions=[t5, t6],
    timestamp=initial_block.timestamp - timedelta(minutes=35),
)


chain = Chain()

assert set(b1.security_hashes) == set()
chain.add_block(block=b1)
assert chain.difficulty == "0001"

chain.add_block(block=b2)
assert set(b2.security_hashes) == {initial_block.get_hash()}
assert chain.difficulty == "0001"

chain.add_block(block=b3)
assert set(b3.security_hashes) == {
    initial_block.get_hash(),
    b1.get_hash(),
}


b4 = Block(
    previous_hash=b3.get_hash(),
    transactions=[Transaction("s1", "r1", 700), Transaction("s1", "r2", 700)],
    timestamp=initial_block.timestamp - timedelta(minutes=30),
)

chain.add_block(block=b4)
assert set(b4.security_hashes) == {
    initial_block.get_hash(),
    b1.get_hash(),
    b2.get_hash(),
}
assert chain.difficulty == "0002"


b5 = Block(
    previous_hash=b4.get_hash(),
    transactions=[Transaction("s1", "r1", 200), Transaction("s1", "r2", 700)],
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


b6 = Block(
    previous_hash=b5.get_hash(),
    transactions=[Transaction("s1", "r1", 200), Transaction("s1", "r2", 700)],
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


b7 = Block(
    previous_hash=b6.get_hash(),
    transactions=[Transaction("s2", "r1", 1200), Transaction("s3", "r2", 1700)],
    timestamp=initial_block.timestamp - timedelta(minutes=15),
)
chain.add_block(block=b7)
assert set(b7.security_hashes) == {
    initial_block.get_hash(),
    b2.get_hash(),
    b3.get_hash(),
    b4.get_hash(),
    b5.get_hash(),
}
assert chain.difficulty == "0002"


b8 = Block(
    previous_hash=b7.get_hash(),
    transactions=[Transaction("s1", "r1", 2200), Transaction("s1", "r3", 7100)],
    timestamp=initial_block.timestamp - timedelta(minutes=10),
)

chain.add_block(block=b8)
assert set(b8.security_hashes) == {
    b1.get_hash(),
    b2.get_hash(),
    b3.get_hash(),
    b4.get_hash(),
    b6.get_hash(),
}
assert chain.difficulty == "0003"


b9 = Block(
    previous_hash=b8.get_hash(),
    transactions=[Transaction("s2", "r2", 3200), Transaction("s1", "r3", 4700)],
    timestamp=initial_block.timestamp - timedelta(minutes=5),
)

chain.add_block(block=b9)
assert set(b9.security_hashes) == {
    b1.get_hash(),
    b2.get_hash(),
    b3.get_hash(),
    b4.get_hash(),
    b5.get_hash(),
}
assert chain.difficulty == "0003"

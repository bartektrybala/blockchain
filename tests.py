from datetime import datetime, timedelta

from schema.schema import Block, Chain, Transaction, initial_block

t1 = Transaction("sender1", "recipient1", 100)
t2 = Transaction("sender2", "recipient2", 1000)
b1 = Block(
    previous_hash=initial_block.get_hash(),
    transactions=[t1, t2],
    timestamp=datetime.now() - timedelta(minutes=45),
)

t3 = Transaction("sender2", "recipient1", 300)
t4 = Transaction("sender1", "recipient2", 1200)
b2 = Block(
    previous_hash=b1.get_hash(),
    transactions=[t3, t4],
    timestamp=datetime.now() - timedelta(minutes=30),
)

t5 = Transaction("sender3", "recipient2", 700)
t6 = Transaction("sender1", "recipient3", 876)
b3 = Block(
    previous_hash=b2.get_hash(),
    transactions=[t5, t6],
    timestamp=datetime.now() - timedelta(minutes=15),
)


chain = Chain()

assert set(chain._select_security_hashes(b1)) == set()
chain.add_block(block=b1)
assert chain.difficulty == "0001"

assert set(chain._select_security_hashes(b2)) == {initial_block.get_hash()}
chain.add_block(block=b2)
assert chain.difficulty == "0001"

assert set(chain._select_security_hashes(b3)) == {
    initial_block.get_hash(),
    b1.get_hash(),
}
chain.add_block(block=b3)


b4 = Block(
    previous_hash=b3.get_hash(),
    transactions=[Transaction("s1", "r1", 700), Transaction("s1", "r2", 700)],
    timestamp=datetime.now() - timedelta(minutes=10),
)

assert set(chain._select_security_hashes(b4)) == {
    initial_block.get_hash(),
    b1.get_hash(),
    b2.get_hash(),
}
chain.add_block(block=b4)
assert chain.difficulty == "0002"


b5 = Block(
    previous_hash=b4.get_hash(),
    transactions=[Transaction("s1", "r1", 200), Transaction("s1", "r2", 700)],
    timestamp=datetime.now() - timedelta(minutes=5),
)

assert set(chain._select_security_hashes(b5)) == {
    initial_block.get_hash(),
    b1.get_hash(),
    b2.get_hash(),
    b3.get_hash(),
}
chain.add_block(block=b5)
assert chain.difficulty == "0002"


b6 = Block(
    previous_hash=b5.get_hash(),
    transactions=[Transaction("s1", "r1", 200), Transaction("s1", "r2", 700)],
    timestamp=datetime.now(),
)

assert set(chain._select_security_hashes(b6)) == {
    initial_block.get_hash(),
    b1.get_hash(),
    b2.get_hash(),
    b3.get_hash(),
    b4.get_hash(),
}
chain.add_block(block=b6)
assert chain.difficulty == "0002"

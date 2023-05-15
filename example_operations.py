from example_schema.schema import Chain, Transaction

t1 = Transaction("sender1", "recipient1", 100)
t2 = Transaction("sender2", "recipient2", 1000)

t3 = Transaction("sender2", "recipient1", 300)
t4 = Transaction("sender1", "recipient2", 1200)

t5 = Transaction("sender3", "recipient2", 700)
t6 = Transaction("sender1", "recipient3", 876)


chain = Chain()

chain.add_block(transactions=[t1, t2])
chain.add_block(transactions=[t3, t4])
chain.add_block(transactions=[t5, t6])

print(chain.get_last_block().get_hash())

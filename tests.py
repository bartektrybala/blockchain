from datetime import datetime, timedelta

from schema.schema import Block, Chain, Transaction, initial_block

if __name__ == "__main__":
    # Create a new chain
    chain = Chain()

    # Create the first block
    initial_block = Block(
        previous_hash=b"first_block",
        transactions=[Transaction("satoshi", "genesis", 100)],
        timestamp=datetime.now() - timedelta(hours=1),
    )

    # Add the first block to the chain
    chain.add_block(initial_block, difficulty=2)

    # Add more blocks to the chain
    for i in range(1, 6):
        previous_block = chain.get_last_block()
        transactions = [Transaction(f"sender{i}", f"recipient{i}", i * 10)]
        timestamp = datetime.now()
        new_block = Block(previous_hash=previous_block.get_hash(), transactions=transactions, timestamp=timestamp)
        chain.add_block(new_block, difficulty=2)

    # Validate the chain
    is_valid = chain.validate_chain(difficulty=2)

    # Print the block hashes and chain validation result
    for block in chain.get_blocks():
        block_hash = block.get_hash()
        previous_hash = block.previous_hash
        print(f"Block Hash: {block_hash}")
        print(f"Previous Hash: {previous_hash}")
        print()

    print(f"Chain Validation: {is_valid}")
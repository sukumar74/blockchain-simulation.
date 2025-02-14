# Importing libraries that are needed
import hashlib
import time
import json

# Creating the Block class containing block number, transactions, hash, and nonce
class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    # Method to compute the hash of the block
    def compute_hash(self):
        block_data = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()

# Creating the Blockchain class to manage blocks
class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.pending_transactions = []  # List to store transactions before mining
        self.create_genesis_block()

    # Creating the first block (Genesis Block)
    def create_genesis_block(self):
        genesis_block = Block(0, ["Genesis Transaction"], "0")
        self.chain.append(genesis_block)

    # Method to add a transaction
    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    # Method to mine a new block with pending transactions
    def mine_block(self):
        if not self.pending_transactions:
            return False
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), self.pending_transactions, previous_block.hash)
        self.proof_of_work(new_block)
        self.chain.append(new_block)
        self.pending_transactions = []  # Clear pending transactions
        return True

    # Proof-of-Work implementation
    def proof_of_work(self, block):
        target = '0' * self.difficulty
        while block.hash[:self.difficulty] != target:
            block.nonce += 1
            block.hash = block.compute_hash()

    # Method to validate the integrity of the blockchain
    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.compute_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
            if not current_block.hash.startswith('0' * self.difficulty):
                return False
        return True

# Printing the blockchain
def print_blockchain(blockchain):
    for block in blockchain.chain:
        print(f"Block {block.index}:")
        print(f"Timestamp: {block.timestamp}")
        print(f"Transactions: {block.transactions}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Hash: {block.hash}")
        print(f"Nonce: {block.nonce}")
        print("\n")

if __name__ == "__main__":
    blockchain = Blockchain(difficulty=3)
    blockchain.add_transaction("Alice sends Bob 5 BTC")
    blockchain.add_transaction("Bob sends Charlie 3 BTC")
    blockchain.mine_block()
    
    blockchain.add_transaction("Charlie sends Dave 2 BTC")
    blockchain.mine_block()
    
    print("Original Blockchain:")
    print_blockchain(blockchain)
    print("Blockchain valid?", blockchain.validate_chain())

    # Try to tamper with the second block
    blockchain.chain[1].transactions = ["Eve sends Alice 100 BTC"]
    print("\nAfter tampering, valid?", blockchain.validate_chain())


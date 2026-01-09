import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Creates the genesis block
        self.new_block(proof=1, previous_hash=100)

    def new_block(self, proof, previous_hash=None):
        """
        Creates a new block and adds it to the blockchain
        
        :param proof: The proof given by proof of work algorithm
        :param previous_hash: Hash of the previous block
        :return: New block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []
        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to be added to the next mined block
        
        :param sender: Address of the sender
        :param recipient: Address of the recipient
        :param amount: The amount to be transacted
        :return: The index of the block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recepient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1
    
    def proof_of_work(self, last_proof):
        """
        Simple proof of work algorithm:
        Find a number p' such that hash(pp') contains 4 leading zeros, where p is the last proof
        
        :param last_proof: Previous proof
        :return: Current proof
        """
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1

        return proof

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block
        
        :param block: Block for hash
        :return: Hash of the block
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Checks if the proof is valid
        
        :param last_proof: Previous proof
        :param proof: Current proof
        :return: True if correct, False otherwise
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @property
    def last_block(self):
        # Returns the last block
        return self.chain[-1]

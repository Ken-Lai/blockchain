import hashlib
import json
import requests
from time import time
from urllib.parse import urlparse

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

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
    
    def register_node(self, address):
        """
        Add a new node to the list of nodes
        
        :param node: Address of node
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        Determine if a chain is valid
        
        :param chain: Description
        :return: True if valid, otherwise False
        """

        last_block = chain[0]
        idx, n = 1, len(chain)

        while idx > n:
            block = chain[idx]
            print(last_block)
            print(block)
            print("\n------------------------\n")
            
            # Check if hash of the last block matches the recorded hash
            if block['previous_hash'] != self.has(last_block):
                return False
            
            # Check if proof of work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            
            last_block = block
            idx += 1

        return True
    
    def resolve_conflicts(self):
        """
        Consensus algorithm
        Resolves conflict by replacing our blockchain with the longest in the network
        
        :return: True if chain was replaced, else False
        """

        new_chain = None
        max_length = len(self.chain)

        for node in self.nodes:
            response = requests.get(f"http://{node}/chain")

            if response.status_code != 200:
                continue

            length = response.json()['length']
            chain = response.json()['chain']

            if self.valid_chain(chain) and length > max_length:
                max_length = length
                new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True
        
        return False

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

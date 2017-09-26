from flask import Flask, request
import json, requests, hashlib, datetime
import random
node = Flask(__name__)

# ----------------------------------------------
# Block definition
class Block:
    def __init__(self, index, timestamp, data, prev_hash, new_pofw):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.new_pofw = new_pofw
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha256()
        sha.update(str(self.index) + str(self.timestamp) + str(self.data) +
                    str(self.prev_hash) + str(self.new_pofw))
        return sha.hexdigest()

# Creates the first block in the blockchain
def create_initial_block():
    b = Block(index=0, timestamp=str(datetime.datetime.now()),
        data='none - initial block',
        previous_hash='0', nonce=1)

    return {'index':b.index,
        'timestamp':b.timestamp,
        'data':b.data,
        'nonce':b.nonce,
        'previous_hash':b.previous_hash,
        'hash':b.hash}

# ----------------------------------------------
# presets for node

PORT = 3000
node_transactions = []
peer_addresses = ["http://localhost:4000", "http://localhost:4001", "http://localhost:4002"]
current_miner_address = 'http://localhost:' + str(PORT)

# ----------------------------------------------
# general functions for blockchain

# search chains from peers
def discover_chains():
    chains = []
    for url in peer_addresses:
        block = json.loads(requests.get(url+"/blocks").content)
        chains.append(block)
    return chains

# consensus algorithm that returns the longest chain
def consensus_alg():
    new_chains = discover_chains()
    longest_chain = []
    if new_chains:
    for chain in new_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    return longest_chain

# generates a costly proof-of-concept
def generate_pofw(prev_hash):
    new_pofw, i = None, 0
    NUM_ZEROES = 5
    while not new_pofw:
        sha = hashlib.sha256()
        sha.update(str(prev_hash) + str(i))
        challenge_hash = sha.hexdigest()
        if str(challenge_hash[:NUM_ZEROES]) == '0' * NUM_ZEROES:
            new_pofw = i
        else:
            i += 1
    return new_pofw

# ----------------------------------------------
# Blockchain API

@node.route('/transaction', methods=['POST'])
def transaction():
    if request.method == 'POST':
    incoming_t = request.get_json()
    node_transactions.append(incoming_t)
    print("New Transaction")
    print(f"FROM: {incoming_trans['from']} ", f"TO: {incoming_trans['to']} ", f"AMOUNT: {incoming_trans['amount']} ")
    return "~~ Succesful Transaction Completed."

@node.route('/list-blocks', methods=['GET'])
def get_blocks():
    send_data = json.dumps(blockchain)
    print(send_data + '/n')
    return send_data

@node.route('/mine-block', methods = ['GET'])
def mine():
    EARNINGS = 1
    global node_transactions

    if len(blockchain) == 0:
        raise ValueError("Empty Blockchain")

    #generate proof of concept, reward miner and empty locally stored transactions
    prev_block = blockchain[-1]
    prev_hash = prev_block['hash']
    new_pofw = generate_pofw(prev_hash)
    t = {"amount":EARNINGS, "from": "network", "to":miner_address}
    node_transactions.append(t)

    #create new block for work done
    node_transactions = []
    minedBlock = Block(index=int(prev_block.index)+1,
                        timestamp=str(datetime.datetime.now()),
                        data={"transactions": node_transactions},
                        prev_hash=prev_hash,
                        new_pofw=new_pofw)

    #append block to blockchain
    mined_block = {
        "index":minedBlock.index
        "timestamp":minedBlock.timestamp,
        "data":minedBlock.data,
        "prev_pofw":minedBlock.prev_hash,
        "hash":minedBlock.hash
    }
    blockchain.append(mined_block)
    v = json.dumps(created_block)
    print(v)
    return v

# ----------------------------------------------
# Initialize Server

blockchain = consensus_alg()
if not blockchain:
    blockchain = [create_initial_block()]

node.run(host='0.0.0.0', port=PORT, threaded=True, debug=False)

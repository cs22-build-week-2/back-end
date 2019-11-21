import hashlib
import requests
import sys
import json

from flask import Flask, escape, request, jsonify
import requests


def proof_of_work(last_proof):
    # A valid proof for the provided block
     # block_string = json.dumps(block, sort_keys=True)
    proof = last_proof
    while valid_proof(last_proof, proof) is False:
        proof += 1
    # guess = f'{block_string}{proof}'.encode()
    # guess_hash = hashlib.sha256(guess).hexdigest()
    # print(guess)
    # print(guess_hash)

    return proof


def valid_proof(last_proof, proof):
        # proof here is like salt, block string is the same salt in this case is changing until we find correct hash
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:6] == "000000"


# while True:
#     proof_of_work()


# if __name__ == '__main__':

def mine(headers):
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-treasure-hunt.herokuapp.com/api/bc/"

    coins_mined = 0

    # Run until 1 coin mined
    if coins_mined == 0:
        r = requests.get(url=node + "/last_proof", headers=headers)
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error")
            print("Response returned:")
            print(data)
            print(r)
    else:
        print("You've already mined one coin: " + str(coins_mined))
        print("Response returned:")
        print(data)
        return

    # TODO: Get the LAST proof from `data` and use it to look for a new proof
    new_proof = proof_of_work(data.get('proof'))

    # When found, POST it to the server {"proof": new_proof, "id": id}
    post_data = {"proof": new_proof}

    r = requests.post(url=node + "/mine", json=post_data, headers=headers)
    print(r)
    data = r.json()

    # TODO: If the server responds with a 'message' 'New Block Forged'
    # add 1 to the number of coins mined and print it.  Otherwise,
    # print the message from the server.
    if data.get('messages') == 'New Block Forged':
        coins_mined += 1
        print("Total coins mined: " + str(coins_mined))
    else:
        print(data.get('message'))

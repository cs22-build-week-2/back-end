from flask import Flask, escape, request, jsonify
import requests
import json
import time

from create_map import create_map
from find_short_paths import find_short_paths
from mine import find_proof

app = Flask(__name__)

# How to run Flask App in local environment
# Remember to run the 'pipenv shell'
# If no dependencies, run 'pipenv install --dev'

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/trial')
def trial():
    return unique_rooms

# Get API key request
# Set API key

# Create map
# Have person traverse forever
# Save to a .txt file for every room it goes into
# Then read .txt file, and create a dictionary
# And save the rooms to dictionary.

# { "api_key": "" }
@app.route('/map', methods=['POST'])
def map():
    # Accept an API key
    values = request.get_json()
    initializeURL = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
    headers = {'Authorization': 'Token ' + values['api_key']}

    # Initialize room
    initialize = requests.get(initializeURL, headers = headers)
    initialize_data = initialize.json()

    # Returns a dict with rooms with ids
    rooms_with_ids = create_map(headers, initialize_data, 500)
    print(rooms_with_ids)

    return rooms_with_ids, 200

@app.route('/find_proof', methods=['POST'])
def proof():
    # Accept an API key
    values = request.get_json()
    proofURL = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/'
    mineURL = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/'
    headers = {'Authorization': 'Token ' + values['api_key']}

    proof = requests.get(proofURL, headers=headers)
    proof_data = proof.json()
    print('last proof: ', proof_data)

    found_proof = find_proof(proof_data["proof"])
    print('new proof: ', found_proof)

    # post_data = { "proof": found_proof }
    # mine = requests.get(mineURL, json=post_data, headers=headers)

    # return jsonify(mine), 200
    return jsonify(found_proof), 200

@app.route('/find_path', methods=['POST'])
def path():
    # Accept an API key
    values = request.get_json()
    initializeURL = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
    headers = {'Authorization': 'Token ' + values['api_key']}

    # Initialize room
    initialize = requests.get(initializeURL, headers = headers)
    initialize_data = initialize.json()

    # Room to move to
    final_room = values['move_to']

    path = find_short_paths(initialize_data, final_room, traversing_map)

    return jsonify(path), 200

@app.route('/traverse_path', methods=['POST'])
def traverse_path():
    # Accept an API key
    values = request.get_json()
    initializeURL = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
    moveURL = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/'
    headers = {'Authorization': 'Token ' + values['api_key']}

    # Initialize room
    initialize = requests.get(initializeURL, headers = headers)
    initialize_data = initialize.json()
    cooldown = initialize_data["cooldown"]

    # Room to move to
    final_room = values['move_to']

    path = find_short_paths(initialize_data, final_room, traversing_map)
    for room in path:
        print(cooldown)
        post_data = {"direction": room[0], "next_room_id": room[1]}
        time.sleep(cooldown)
        next_room = requests.post(moveURL, json=post_data, headers=headers)
        next_room_data = next_room.json()
        print(next_room_data)
        cooldown = next_room_data["cooldown"]

    print('---done---')
    return jsonify("done"), 200

if __name__ == '__main__':
    # Loads initial rooms from txt file
    unique_rooms = {}
    traversing_map = {}
    # Loads current dfs_visited from txt file
    with open('map_ids.txt','r') as t:
        traversing_map = json.loads(t.readline())

    # Clean dfs_visited data
    for room in traversing_map.keys():
        if "previous_direction" in traversing_map[room]:
            del traversing_map[room]["previous_direction"]
        traversing_map[room]['room_id'] = room 


    # Loads txt file into dict
    with open('map.txt','r') as f:
        for cnt, line in enumerate(f):
            room = json.loads(line)
            unique_rooms[room["room_id"]] = room

    print(traversing_map)
    # print(unique_rooms)

    # Keep last
    app.run(host='0.0.0.0', port=5000)

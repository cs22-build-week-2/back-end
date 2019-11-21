from flask import Flask, escape, request, jsonify
import requests
import json

from create_map import create_map
from find_short_paths import find_short_paths

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

<<<<<<< HEAD

=======
# { "api_key": "" }
>>>>>>> b0181c6f6ab1772eb8f4edc86c7390b90e930a9d
@app.route('/map', methods=['POST'])
def map():
    # Accept an API key
    values = request.get_json()
    initializeURL = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
    headers = {'Authorization': 'Token ' + values['api_key']}

<<<<<<< HEAD
    initialize = requests.get(initializeURL, headers=headers)
    initializeData = initialize.json()
=======
    # Initialize room
    initialize = requests.get(initializeURL, headers = headers)
    initialize_data = initialize.json()

    # Returns a dict with rooms with ids # traversing_map
    rooms_with_ids = create_map(headers, initialize_data, 500)
    print(rooms_with_ids)

    return rooms_with_ids, 200
>>>>>>> b0181c6f6ab1772eb8f4edc86c7390b90e930a9d

@app.route('/find_path', methods=['POST'])
def path():
    # Accept an API key
    values = request.get_json()
    initializeURL = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
    headers = {'Authorization': 'Token ' + values['api_key']}

    # Initialize room
    initialize = requests.get(initializeURL, headers = headers)
    initialize_data = initialize.json()

    find_short_paths(initialize_data, unique_rooms)

    return jsonify(path), 200


@app.route('/mine', methods={'POST'})
def get_coin():
    # accept an API key
    values = request.get_json()
    # initializeURL = 'https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/'
    headers = {'Authorization': 'Token ' + values['api_key']}

    # initialize = requests.post(initializeURL, headers=headers)
    # initializeData = initialize.json()
    def mine(headers)

    # not sure what to return here
    return jsonify(initializeData), 200


if __name__ == '__main__':
<<<<<<< HEAD
=======
    # Loads initial rooms from txt file
    unique_rooms = {}
    # traversing_map = {}
    # Loads current dfs_visited from txt file
    # with open('map_ids.txt','r') as t:
    #     traversing_map = json.loads(t.readline())

    # Loads txt file into dict
    with open('map.txt','r') as f:
        for cnt, line in enumerate(f):
            room = json.loads(line)
            unique_rooms[room["room_id"]] = room

    # print(traversing_map)
    print(unique_rooms)

    # Keep last
>>>>>>> b0181c6f6ab1772eb8f4edc86c7390b90e930a9d
    app.run(host='0.0.0.0', port=5000)

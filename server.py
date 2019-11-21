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

    return jsonify(rooms_with_ids), 200

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

if __name__ == '__main__':
    # Loads initial rooms from txt file
    unique_rooms = {}

    # Loads txt file into dict
    with open('map.txt','r') as f:
        for cnt, line in enumerate(f):
            room = json.loads(line)
            print(room)
            unique_rooms[room["room_id"]] = room

    # Keep last
    app.run(host='0.0.0.0', port=5000)

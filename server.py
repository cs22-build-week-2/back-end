from flask import Flask, escape, request, jsonify
import requests

from create_map import create_map
app = Flask(__name__)

# How to run Flask App in local environment
# Remember to run the 'pipenv shell'
# If no dependencies, run 'pipenv install --dev'

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

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

    initialize = requests.get(initializeURL, headers = headers)
    initialize_data = initialize.json()

    rooms_with_ids = create_map(headers, initialize_data, 500)

    return jsonify(rooms_with_ids), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
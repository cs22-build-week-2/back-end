from flask import Flask, escape, request, jsonify
import requests

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


@app.route('/map', methods=['POST'])
def create_map():
    # Accept an API key
    values = request.get_json()
    initializeURL = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'
    headers = {'Authorization': 'Token ' + values['api_key']}

    initialize = requests.get(initializeURL, headers=headers)
    initializeData = initialize.json()

    return jsonify(initializeData), 200


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
    app.run(host='0.0.0.0', port=5000)

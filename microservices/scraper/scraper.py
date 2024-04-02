from flask import Flask, request, jsonify
from flask_cors import CORS

import requests
import json

import os, sys
from os import environ

from invokes import invoke_http

# import schedule
import time

# Init flask app
app = Flask(__name__)
CORS(app)


# Declare ENV vars
# luft_URL = "http://localhost:5004/getLHflights/today"
ryanair_URL = environ.get('ryanair_URL')
lufthansa_URL = environ.get('lufthansa_URL')
flight_URL = environ.get('flight_URL')

# Get the JSON data from the API
# response = requests.get(luft_URL)
# data = response.json()

# @app.route('/insertflights', methods=['POST'], json=data)

# xinsert_flights_URL = "http://your-api-url/insertflights"


@app.route("/scrapeAPIs")
def scrapeAPI():
    # Call lufthansa API
    insert_LH_flight = invoke_http(lufthansa_URL, method='GET')

    if insert_LH_flight['code'] == 200:
        data = insert_LH_flight['data']
        all_LHresponses = []

        for date, flights in data.items():
            all_LHresponses.extend(flights)

        print(all_LHresponses)
    else:
        print("Failed to get responses. Response code:", insert_LH_flight['code'])


    # Call ryanair API
    insert_FR_flight = invoke_http(ryanair_URL, method='GET')['data']

    print(insert_FR_flight)

    # Merge both lists
    all_flights = {"flight": insert_FR_flight + all_LHresponses}

    print(all_flights)

    # Insert into flights DB
    results = invoke_http(flight_URL, method='POST', json=all_flights)

    return jsonify(results)


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)



# # Send the data to the /insertflights endpoint
# sendresponse = requests.post('/insertflights', methods=['POST'], json=data)

# @app.route("/insertflights", methods=['POST'])
# def insertflights():

# # Check if the request was successful
#     if sendresponse.status_code == 200:
#         print('Data sent successfully')
#     else:
#         print('Failed to send data', sendresponse.status_code, sendresponse.text)


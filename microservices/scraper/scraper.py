from flask import Flask, jsonify
from flask_cors import CORS
from os import environ
from invokes import invoke_http
import json

app = Flask(__name__)
CORS(app)

ryanair_URL = environ.get('ryanair_URL')
lufthansa_URL = environ.get('lufthansa_URL')
flight_URL = environ.get('flight_URL')
seat_URL = environ.get('seat_URL')

@app.route("/scrapeAPIs")
def scrapeAPI():
    all_flights = []

    # Call Lufthansa API
    insert_LH_flight = invoke_http(lufthansa_URL, method='GET')
    if insert_LH_flight['code'] == 200:
        data = insert_LH_flight['data']
        for date, flights in data.items():
            all_flights.extend(flights)
    else:
        print("Failed to get responses from Lufthansa API. Response code:", insert_LH_flight['code'])

    # Call Ryanair API
    insert_FR_flight = invoke_http(ryanair_URL, method='GET')
    if insert_FR_flight['code'] == 200:
        all_flights.extend(insert_FR_flight['data'])
    else:
        print("Failed to get responses from Ryanair API. Response code:", insert_FR_flight['code'])

    # Merge both lists
    all_flights_data = {"flight": all_flights}

    # Read seat layout from seat_layout.json
    with open('seat_layout.json', 'r') as f:
        seat_layout = json.load(f)

    flight_seats = {}

    for flight in all_flights_data['flight']:
        fid = flight['FID']
        flight_seats[fid] = [{'seatcol': seat['seatcol'], 'seatnum': seat['seatrow']} for seat in seat_layout]

    # Insert into flights DB
    flight_results = invoke_http(flight_URL, method='POST', json=all_flights_data)

    # Insert into seats DB
    seat_results = invoke_http(seat_URL, method='POST', json=flight_seats)

    results = flight_results + seat_results

    return jsonify(results)

if __name__ == "__main__":
    print("Starting the scraper service...")
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


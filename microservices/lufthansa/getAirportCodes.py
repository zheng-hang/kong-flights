import requests
import json

# Current airlines
# LH - Lufthansa
# EN - Air Dolomiti
# LX - Swiss
# S - Austrian
# WK - Edelweiss
# SN - Brussels Airlines


# Set the URL for the API endpoint
url = "https://api.lufthansa.com/v1/flight-schedules/flightschedules/passenger"

# Set the parameters for the GET request
params = {
    "airlines": "SN",
    "startDate": "01APR24",
    "endDate": "08APR24",
    "daysOfOperation": "1234567",
    "timeMode": "UTC"
}

# Set the headers, including the Authorization token
headers = {
    "accept": "application/json",
    "Authorization": "Bearer bsey8jy2b9skmcrkn2t4axkt"
}

# Make the GET request
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code in [200,206]:
    # Parse the response JSON if needed
    data = response.json()
    print("data received")
else:
    print(f"Failed to retrieve data: {response.status_code}")


import json
import os

def update_flight_file_with_new_airline(data, output_filename):
    # Try to load existing data if the file exists
    if os.path.exists(output_filename):
        with open(output_filename, 'r') as outfile:
            try:
                existing_flights = json.load(outfile)
            except json.JSONDecodeError:  # In case the file is empty or invalid
                existing_flights = {}
    else:
        existing_flights = {}


    for entry in data:
        airline = entry['airline']
        legs = entry['legs']

        if len(legs) != 1:
            continue

        if airline not in existing_flights:
            existing_flights[airline] = {'Departure': set(), 'Arrival': set()}

        existing_flights[airline]['Departure'].add(legs[0]['origin'])
        existing_flights[airline]['Arrival'].add(legs[0]['destination'])

    # Prepare the data for JSON serialization
    for airline in existing_flights:
        existing_flights[airline]['Departure'] = list(existing_flights[airline]['Departure'])
        existing_flights[airline]['Arrival'] = list(existing_flights[airline]['Arrival'])

    # Write the updated information back to the .json file
    with open(output_filename, 'w') as outfile:
        json.dump(existing_flights, outfile, indent=4)


# Example usage
output_filename = 'processed_flights.json'
update_flight_file_with_new_airline(data, output_filename)
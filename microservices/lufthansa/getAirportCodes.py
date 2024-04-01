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
    "airlines": "LH",
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



def filter_flights(data, output_file):

    filtered_data = {}
    for entry in data:
        legs = entry.get('legs', [])
        if len(legs) == 1:
            airline = entry['airline']
            departure = legs[0]['origin']
            arrival = legs[0]['destination']
            pair = {"Departure": departure, "Arrival": arrival}

            if airline not in filtered_data:
                filtered_data[airline] = set()

            filtered_data[airline].add((departure, arrival))

    for airline, pairs in filtered_data.items():
        filtered_data[airline] = [{"Departure": dep, "Arrival": arr} for dep, arr in pairs]

    with open(output_file, 'w') as f:
        json.dump(filtered_data, f, indent=4)


# Usage example
filter_flights(data, './arrDep.json')



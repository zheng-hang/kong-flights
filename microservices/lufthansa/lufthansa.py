from flask import Flask, request, jsonify
from os import environ
from flask_cors import CORS

import requests
import json
import time
from datetime import datetime, timedelta

from geopy.distance import geodesic
from pyairports.airports import Airports
import random

app = Flask(__name__)
airports = Airports()


# Get previously loaded Arrival Departure codes from Lufthansa API
with open("./arrDep.json", 'r') as f:
    airportcodes = json.load(f)
    print("loaded")



# Current airlines
# LH - Lufthansa
# EN - Air Dolomiti
# LX - Swiss
# S - Austrian
# WK - Edelweiss
# SN - Brussels Airlines

    

# Randomise Price
def get_distance(airport1, airport2):
    lat1 = airports.airport_iata(airport1).lat
    lon1 = airports.airport_iata(airport1).lon
    lat2 = airports.airport_iata(airport2).lat
    lon2 = airports.airport_iata(airport2).lon
    coords1 = (lat1, lon1)
    coords2 = (lat2, lon2)
    distance = geodesic(coords1, coords2).kilometers
    return distance

def estimate_price(distance, price_per_km):
    return distance * price_per_km

def randomize_price(price_estimate):
    max_variation = price_estimate * 0.05  # 5% of the estimated price
    return price_estimate + random.uniform(-max_variation, max_variation)

def calculate_and_randomize_price(airport1, airport2):
    PRICE_PER_KM = 0.15

    distance = get_distance(airport1, airport2)
    price_estimate = estimate_price(distance, PRICE_PER_KM)
    randomized_price = randomize_price(price_estimate)
    return round(randomized_price,2)





# Get relevant details from passed schedule
def extract_flight_info(schedule):
    try:
        if 'Flight' in schedule:  # Check if schedule is a single flight
            flight = schedule['Flight']
            flight_number = f"{flight['MarketingCarrier']['AirlineID']} {flight['MarketingCarrier']['FlightNumber']}"
            departure_time = flight['Departure']['ScheduledTimeLocal']['DateTime']
            duration_parts = schedule['TotalJourney']['Duration'].split('H')
            hours = int(duration_parts[0][2:]) if duration_parts[0] else 0  # Handle empty duration
            minutes = int(duration_parts[1][:-1]) if duration_parts[1] else 0  # Handle empty duration
            dep_airport_code = flight['Departure']['AirportCode']
            arr_airport_code = flight['Arrival']['AirportCode']
            
            return flight_number, {
                'Airline': flight['MarketingCarrier']['AirlineID'],
                'DepartureLoc': airports.airport_iata(dep_airport_code)[1],
                'ArrivalLoc': airports.airport_iata(arr_airport_code)[1],
                'Date': departure_time[:10],
                'DepartureTime': departure_time[11:16],
                'Duration': hours * 60 + minutes,
                'Price': calculate_and_randomize_price(dep_airport_code, arr_airport_code),
                'DepAirportCode': dep_airport_code,
                'ArrAirportCode': arr_airport_code
            }
        elif isinstance(schedule, list):  # Check if schedule is a list of flights
            flights_data = []
            for flight_schedule in schedule:
                flight_data = extract_flight_info(flight_schedule)
                if flight_data:
                    flights_data.append(flight_data)
            return flights_data
        else:
            print("Invalid schedule format.")
            return None
    except KeyError as e:
        print(f"KeyError: {e}")
        return None
    except ValueError as e:
        print(f"ValueError: {e}")
        return None



# Call API to get flight schedules
def get_flight_schedules(airport_pairs, datetime, api_key):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    
    all_flights = {}
    for airline, pairs in airport_pairs.items():
        for pair in pairs:
            origin = pair['Departure']
            destination = pair['Arrival']
            airportcodes_url = f'https://api.lufthansa.com/v1/operations/schedules/{origin}/{destination}/{datetime}?directFlights=1'
            
            response = requests.get(airportcodes_url, headers=headers)
            if response.status_code == 200:
                try:
                    schedule = response.json()['ScheduleResource']['Schedule']
                    print(type(schedule))
                    if isinstance(schedule, list):
                        print('list')
                        for flight_schedule in schedule:
                            flightNum, flight_info = extract_flight_info(flight_schedule)
                            if flight_info:
                                all_flights[flightNum] = flight_info
                    elif isinstance(schedule, dict):  # Only one flight for the path
                        print('dict')
                        flightNum, flight_info = extract_flight_info(schedule)
                        if flight_info:
                            all_flights[flightNum] = flight_info
                    else:
                        print("Invalid schedule format.")
                except KeyError:
                    print(schedule)
                    print(response.json())
                    print(f"Failed to retrieve schedule for {airline} flight from {origin} to {destination}.")
            else:
                print(f"Failed to retrieve schedule for {airline} flight from {origin} to {destination}. {response.status_code}")

            # Ensure no more than 5 calls per second
            time.sleep(0.2)
    
    return all_flights





# Flask path to call API and get flights from Lufthansa

@app.route("/getLHflights")
def getFlightTdyTo7days():
    # Define the date range
    datetime_format = '%Y-%m-%d'
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=7)

    # Convert dates to the required format
    start_date_str = start_date.strftime(datetime_format)
    end_date_str = end_date.strftime(datetime_format)
    date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    # Call the function for each date and store the results
    all_flights_data = {}
    for date in date_range:
        formatted_date = date.strftime('%Y-%m-%d')
        flights_data = get_flight_schedules(airportcodes, formatted_date, API_KEY)
        all_flights_data[formatted_date] = flights_data

    # Save the data to a JSON file
    with open('flightsLH.json', 'w') as outfile:
        json.dump(all_flights_data, outfile, indent=4)

    print("Flight data saved to 'flightsLH.json'")

    # Return values to Scraper
    return jsonify(
            {
                "code": 200,
                "data": all_flights_data
            }
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
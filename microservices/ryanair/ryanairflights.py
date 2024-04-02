# departureTime: A datetime object representing the departure time of the flight.
# flightNumber: A string representing the flight number.
# price: A float representing the price of the flight.
# currency: A string representing the currency of the price.
# origin: A string representing the departure airport code.
# originFull: A string representing the full name of the departure airport.
# destination: A string representing the arrival airport code.
# destinationFull: A string representing the full name of the arrival airport.
from flask import Flask, jsonify

import json
import math
from datetime import datetime, timedelta

from geopy.distance import geodesic
from pyairports.airports import Airports
from pyairports.airports import AirportNotFoundException
import random
from forex_python.converter import CurrencyRates
from ryanair import Ryanair
from ryanair.types import Flight

airports = Airports()
api = Ryanair(currency="EUR")
app = Flask(__name__)

# Randomise duration
with open("./ryanair_codes.json", 'r') as file:
    data = json.load(file)
    airportcodes = data
    print('loaded')


def convert_to_sgd(price, currency='EUR'):
    c = CurrencyRates()
    rate = c.get_rate(currency, 'SGD')
    return round(price * rate, 2)


def get_distance_between_airports(airport1, airport2):
    lat1 = airports.airport_iata(airport1).lat
    lon1 = airports.airport_iata(airport1).lon
    lat2 = airports.airport_iata(airport2).lat
    lon2 = airports.airport_iata(airport2).lon
    coords1 = (lat1, lon1)
    coords2 = (lat2, lon2)
    distance = geodesic(coords1, coords2).kilometers
    return distance

def estimate_duration(distance, km_per_min):
    return distance / km_per_min

def randomize_duration(duration_estimate):
    max_variation = duration_estimate * 0.05  # 5% of the estimated duration
    return duration_estimate + random.uniform(0, max_variation)

def calculate_and_randomize_duration(airport1, airport2, km_per_min):
    distance = get_distance_between_airports(airport1, airport2)
    duration_estimate = estimate_duration(distance, km_per_min)
    randomized_duration = randomize_duration(duration_estimate)
    rounded_duration = math.ceil(randomized_duration / 5) * 5  # Round up to nearest multiple of 5
    return rounded_duration



def get_flight_info(airport_codes, date):
    flights = []
    for airport_code in airport_codes:
        departure = airport_code
        response = api.get_cheapest_flights(departure, date, date + timedelta(days=1))
        for flight in response:
            try:
                print(f"Loading flight {flight.flightNumber} for {flight.origin} to {flight.destination}")
                price_sgd = convert_to_sgd(flight.price)
                flights.append({
                    'FID': flight.flightNumber,
                    'Airline': 'Ryanair',
                    'DepartureLoc': airports.airport_iata(flight.origin).city,
                    'ArrivalLoc': airports.airport_iata(flight.destination).city,
                    'Date': flight.departureTime.strftime('%Y-%m-%d'),
                    'DepartureTime': flight.departureTime.strftime('%H:%M'),
                    'Duration': calculate_and_randomize_duration(flight.origin, flight.destination, 0.8),  # Assuming 0.8 km/min
                    'Price': price_sgd,
                    'DepAirportCode': flight.origin,
                    'ArrAirportCode': flight.destination
                })
            except KeyError as e:
                print(f"KeyError: {e}")
                pass
            except ValueError as e:
                print(f"ValueError: {e}")
                pass
            except AirportNotFoundException as e:
                print(f"AirportNotFoundException: {e}")
                pass

    return flights

@app.route("/getFRflights/today")
def run_today():
    date = datetime.now().date()

    # Usage example
    flights = get_flight_info(airportcodes, date)

    # Write flights to JSON file
    with open('flightsFR.json', 'w') as json_file:
        json.dump(flights, json_file, indent=4)

    print("Flight data for today saved to 'flightsLH.json'")

    # Return values to Scraper
    return jsonify(
            {
                "code": 200,
                "data": date
            }
        )


@app.route("/getLHflights/7days")
def get_flight_info_for_7_days(airport_codes):
    for i in range(7):
        date = datetime.now().date() + timedelta(days=i)
        flights = get_flight_info(airport_codes, date)

    with open('flightsFR.json', 'w') as json_file:
        json.dump(flights, json_file, indent=4)

    print("Flight data for today saved to 'flightsLH.json'")

    # Return values to Scraper
    return jsonify(
            {
                "code": 200,
                "data": date
            }
        )



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



from geopy.distance import geodesic
from pyairports.airports import Airports
import random

airports = Airports()

import random
from geopy.distance import geodesic

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
    print(duration_estimate)
    randomized_duration = randomize_duration(duration_estimate)
    return randomized_duration


# Example usage
airport1 = 'SIN'  # Singapore Changi Airport
airport2 = 'KUL'  # John F. Kennedy International Airport
distance_per_km = 0.5  # Hypothetical distance per kilometer
randomized_distance = calculate_and_randomize_price(airport1, airport2, price_per_km)
print(f"Randomized price: ${randomized_price:.2f}")

# print(airports.airport_iata(airport1).lat)

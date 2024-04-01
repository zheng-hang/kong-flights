from geopy.distance import geodesic
from pyairports.airports import Airports
import random

airports = Airports()

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
    max_variation = price_estimate * 0.1  # 10% of the estimated price
    return price_estimate + random.uniform(-max_variation, max_variation)

def calculate_and_randomize_price(airport1, airport2, price_per_km):
    distance = get_distance(airport1, airport2)
    price_estimate = estimate_price(distance, price_per_km)
    print(price_estimate)
    randomized_price = randomize_price(price_estimate)
    return randomized_price

# Example usage
airport1 = 'SIN'  # Singapore Changi Airport
airport2 = 'KUL'  # John F. Kennedy International Airport
price_per_km = 0.5  # Hypothetical price per kilometer
randomized_price = calculate_and_randomize_price(airport1, airport2, price_per_km)
print(f"Randomized price: ${randomized_price:.2f}")

# print(airports.airport_iata(airport1).lat)

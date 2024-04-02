from datetime import datetime, timedelta
from ryanair import Ryanair
from ryanair.types import Flight

api = Ryanair(currency="EUR")  # Euro currency, so could also be GBP etc. also
tomorrow = datetime.today().date() + timedelta(days=1)

# arrival_airport_codes = [
#     'VIE','CFU', 'WRO',
#     'ARN', 'POZ', 'PMO', 'SKG', 'PLQ', 'PMI', 'VLC',
#     'GDN', 'RIX', 'BUD', 'ZAG', 'DLM', 'ALC', 'BRU'
# ]


# for each in arrival_airport_codes:
#     flights = api.get_cheapest_flights(each, tomorrow, tomorrow + timedelta(days=1))
#     print(flights)
#     print("")

# # Returns a list of Flight namedtuples
# flight: Flight = flights[0]
# print(flight)  # Flight(departureTime=datetime.datetime(2023, 3, 12, 17, 0), flightNumber='FR9717', price=31.99, currency='EUR' origin='DUB', originFull='Dublin, Ireland', destination='GOA', destinationFull='Genoa, Italy')
# print(flight.price)  # 9.78


import json
from datetime import datetime, timedelta
from typing import List, Dict

# Assume api.get_cheapest_flights(<departure>, tomorrow, tomorrow + timedelta(days=1)) is a placeholder for your actual API call

class Flight:
    def __init__(self, departureTime, flightNumber, price, currency, origin, originFull, destination, destinationFull):
        self.departureTime = departureTime
        self.flightNumber = flightNumber
        self.price = price
        self.currency = currency
        self.origin = origin
        self.originFull = originFull
        self.destination = destination
        self.destinationFull = destinationFull

    def __repr__(self):
        return f"Flight(departureTime={self.departureTime}, flightNumber='{self.flightNumber}', price={self.price}, currency='{self.currency}', origin='{self.origin}', originFull='{self.originFull}', destination='{self.destination}', destinationFull='{self.destinationFull}')"

def get_cheapest_flights(departure: str, start_date: datetime, end_date: datetime) -> List[Flight]:
    # Placeholder for your actual API call
    return []

def get_unique_airport_codes(departure_airport_codes: List[str], date: datetime) -> List[str]:
    unique_airport_codes = set()

    for departure in departure_airport_codes:
        cheapest_flights = api.get_cheapest_flights(departure, date, date + timedelta(days=1))
        for flight in cheapest_flights:
            unique_airport_codes.add(flight.origin)
            unique_airport_codes.add(flight.destination)

    return list(unique_airport_codes)

# Example usage
arrival_airport_codes = [
    'VIE','CFU', 'WRO',
    'ARN', 'POZ', 'PMO', 'SKG', 'PLQ', 'PMI', 'VLC',
    'GDN', 'RIX', 'BUD', 'ZAG', 'DLM', 'ALC', 'BRU'
]

date = datetime(2024, 4, 3)  # Example date

unique_airport_codes = get_unique_airport_codes(arrival_airport_codes, date)

# Write unique_airport_codes to a JSON file
with open('ryanair_codes.json', 'w') as f:
    json.dump(unique_airport_codes, f, indent=4)

print("Unique airport codes written to airport_codes.json")
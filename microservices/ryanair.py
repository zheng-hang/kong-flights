from datetime import datetime, timedelta
from ryanair import Ryanair
from ryanair.types import Flight

api = Ryanair(currency="EUR")  # Euro currency, so could also be GBP etc. also
tomorrow = datetime.today().date() + timedelta(days=1)

flights = api.get_cheapest_flights("DUB", tomorrow, tomorrow + timedelta(days=1))

# Returns a list of Flight namedtuples
flight: Flight = flights[0]
print(flight)  # Flight(departureTime=datetime.datetime(2023, 3, 12, 17, 0), flightNumber='FR9717', price=31.99, currency='EUR' origin='DUB', originFull='Dublin, Ireland', destination='GOA', destinationFull='Genoa, Italy')
print(flight.price)  # 9.78


# # When
# def extract_airport_codes(json_data):
#     airports = json_data.get('AirportResource', {}).get('Airports', {}).get('Airport', [])
#     airport_codes = [airport.get('AirportCode', '') for airport in airports]
#     return airport_codes

# # def postRequ(url, headers):
# #     return requests.post(url, headers=headers, json=data)

# # Replace 'YOUR_API_KEY' with your actual SIA API key
# API_KEY = 'uuabey8rvxfbvznqqhtqt6je'

# # offset = 200
# # origin = "FRA"
# # destination = 'HAM'
# # datetime = '2024-04-01'

# #SEARCH 
# #Params:
# clientUUID = uuid.uuid4()
# origin = "SIN"
# destination = "BKK"
# date_time = "2024-11-01"
# date_return = "2024-11-10"

# # airportcodes_url = 'https://api.lufthansa.com/v1/operations/schedules/'+origin+'/'+destination+'/'+datetime+'?directFlights=1'
# URL = 'https://apigw.singaporeair.com/api/uat/v1/commercial/flightavailability/get'

# headers = {
#     'Authorization': "q4g682kpvty6ggxat9pxs953",
#     'Content-Type': 'application/json'
# }

# data = {
#     "clientUUID": "05b2fa78-a0f8-4357-97fe-d18506618c3f",
#     "request": {
#         "itineraryDetails": [
#             {
#                 "originAirportCode": "SIN",
#                 "destinationAirportCode": "BKK",
#                 "departureDate": "2024-11-01",
#                 "returnDate": "2024-11-10"
#             }
#         ],
#         "cabinClass": "Y",
#         "adultCount": 1,
#         "childCount": 0,
#         "infantCount": 0
#     }
# }

# # headers = {
# #     'apikey': f'Bearer {API_KEY}',
# #     'Content-Type': 'application/json'
# # }
# # data = {
# #     "clientUUID": {clientUUID},
# #     "request": {
# #         "itineraryDetails": [
# #             {
# #                 "originAirportCode": {origin},
# #                 "destinationAirportCode": {destination},
# #                 "departureDate": {date_time},
# #                 "returnDate": {date_return}
# #             }
# #         ],
# #         "cabinClass": "Y",
# #         "adultCount": 1,
# #         "childCount": 0,
# #         "infantCount": 0
# #     }
# # }

# # airportcodes = ['AAA', 'AAB', 'AAC', 'AAD', 'AAE', 'AAF', 'AAG', 'AAH', 'AAI', 'AAJ', 'AAK', 'AAL', 'AAM', 'AAN', 'AAO', 'AAP', 'AAQ', 'AAR', 'AAS', 'AAT', 'AAU', 'AAV', 'AAW', 'AAX', 'AAY', 'AAZ', 'ABA', 'ABB', 'ABC', 'ABD', 'ABE', 'ABF', 'ABG', 'ABH', 'ABI', 'ABJ', 'ABK', 'ABL', 'ABM', 'ABN', 'ABO', 'ABP', 'ABQ', 'ABR', 'ABS', 'ABT', 'ABU', 'ABV', 'ABW', 'ABX', 'ABY', 'ABZ', 'ACA', 'ACB', 'ACC', 'ACD', 'ACE', 'ACF', 'ACH', 'ACI', 'ACJ', 'ACK', 'ACL', 'ACM', 'ACN', 'ACO', 'ACP', 'ACQ', 'ACR', 'ACS', 'ACT', 'ACU', 'ACV', 'ACX', 'ACY', 'ACZ', 'ADA', 'ADB', 'ADC', 'ADD', 'ADE', 'ADF', 'ADG', 'ADH', 'ADI', 'ADJ', 'ADK', 'ADL', 'ADM', 'ADN', 'ADO', 'ADP', 'ADQ', 'ADR', 'ADS', 'ADT', 'ADU', 'ADV', 'ADW', 'ADX', 'ADX', 'ADY', 'ADZ', 'AEA', 'AEB', 'AED', 'AEE', 'AEG', 'AEH', 'AEI', 'AEJ', 'AEK', 'AEL', 'AEM', 'AEN', 'AEO', 'AEP', 'AEQ', 'AER', 'AES', 'AET', 'AEU', 'AEX', 'AEY', 'AFA', 'AFD', 'AFF', 'AFI', 'AFK', 'AFL', 'AFN', 'AFO', 'AFR', 'AFS', 'AFT', 'AFU', 'AFW', 
# # 'AFY', 'AFZ', 'AGA', 'AGB', 'AGC', 'AGD', 'AGE', 'AGF', 'AGG', 'AGH', 'AGI', 'AGJ', 'AGK', 'AGL', 'AGM', 'AGN', 'AGO', 'AGP', 'AGQ', 'AGR', 'AGS', 'AGT', 'AGU', 'AGV', 'AGW', 'AGX', 'AGY', 'AGZ', 'AHA', 'AHB', 'AHC', 'AHD', 'AHE', 'AHF', 'AHH', 'AHI', 'AHJ', 'AHL', 'AHM', 'AHN', 'AHO', 'AHS', 'AHT', 'AHU', 'AHW', 'AHY', 'AHZ', 'AIA', 'AIB', 'AIC', 'AID', 'AIE', 'AIF', 'AIG', 'AIH', 'AII', 'AIK', 'AIL', 'AIM', 'AIN', 'AIO', 'AIP', 'AIR', 'AIS', 'AIT', 'AIU', 'AIV', 'AIW', 'AIX']
# print(requests.post(url=URL, headers=headers, json=data))
# print('hi')
# response = requests.post(URL, headers=headers, json=data)


# if response.status_code == 200:
#     data = response.json()
#     # Process the data as needed
#     # airportcodes.extend(extract_airport_codes(data))
#     print(data)
# else:
#     print(f'Failed to fetch data: {response.status_code}, {response.text}')

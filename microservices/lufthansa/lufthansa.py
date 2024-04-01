import requests
import json

# When
def extract_airport_codes(json_data):
    airports = json_data.get('AirportResource', {}).get('Airports', {}).get('Airport', [])
    airport_codes = [airport.get('AirportCode', '') for airport in airports]
    return airport_codes

def getResponse(url, headers):
    return requests.get(url, headers=headers)


# Replace 'YOUR_API_KEY' with your actual Lufthansa API key
API_KEY = '35h82u5sty2qzdem97yjfsg9'

offset = 200
origin = "FRA"
destination = 'HAM'
datetime = '2024-04-01'

airportcodes_url = 'https://api.lufthansa.com/v1/operations/schedules/'+origin+'/'+destination+'/'+datetime+'?directFlights=1'
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json'
}

# Current airlines
# LH - Lufthansa
# EN - Air Dolomiti
# LX - Swiss
# S - Austrian
# WK - Edelweiss
# SN - Brussels Airlines

# airportcodes = ['AAA', 'AAB', 'AAC', 'AAD', 'AAE', 'AAF', 'AAG', 'AAH', 'AAI', 'AAJ', 'AAK', 'AAL', 'AAM', 'AAN', 'AAO', 'AAP', 'AAQ', 'AAR', 'AAS', 'AAT', 'AAU', 'AAV', 'AAW', 'AAX', 'AAY', 'AAZ', 'ABA', 'ABB', 'ABC', 'ABD', 'ABE', 'ABF', 'ABG', 'ABH', 'ABI', 'ABJ', 'ABK', 'ABL', 'ABM', 'ABN', 'ABO', 'ABP', 'ABQ', 'ABR', 'ABS', 'ABT', 'ABU', 'ABV', 'ABW', 'ABX', 'ABY', 'ABZ', 'ACA', 'ACB', 'ACC', 'ACD', 'ACE', 'ACF', 'ACH', 'ACI', 'ACJ', 'ACK', 'ACL', 'ACM', 'ACN', 'ACO', 'ACP', 'ACQ', 'ACR', 'ACS', 'ACT', 'ACU', 'ACV', 'ACX', 'ACY', 'ACZ', 'ADA', 'ADB', 'ADC', 'ADD', 'ADE', 'ADF', 'ADG', 'ADH', 'ADI', 'ADJ', 'ADK', 'ADL', 'ADM', 'ADN', 'ADO', 'ADP', 'ADQ', 'ADR', 'ADS', 'ADT', 'ADU', 'ADV', 'ADW', 'ADX', 'ADX', 'ADY', 'ADZ', 'AEA', 'AEB', 'AED', 'AEE', 'AEG', 'AEH', 'AEI', 'AEJ', 'AEK', 'AEL', 'AEM', 'AEN', 'AEO', 'AEP', 'AEQ', 'AER', 'AES', 'AET', 'AEU', 'AEX', 'AEY', 'AFA', 'AFD', 'AFF', 'AFI', 'AFK', 'AFL', 'AFN', 'AFO', 'AFR', 'AFS', 'AFT', 'AFU', 'AFW', 
# 'AFY', 'AFZ', 'AGA', 'AGB', 'AGC', 'AGD', 'AGE', 'AGF', 'AGG', 'AGH', 'AGI', 'AGJ', 'AGK', 'AGL', 'AGM', 'AGN', 'AGO', 'AGP', 'AGQ', 'AGR', 'AGS', 'AGT', 'AGU', 'AGV', 'AGW', 'AGX', 'AGY', 'AGZ', 'AHA', 'AHB', 'AHC', 'AHD', 'AHE', 'AHF', 'AHH', 'AHI', 'AHJ', 'AHL', 'AHM', 'AHN', 'AHO', 'AHS', 'AHT', 'AHU', 'AHW', 'AHY', 'AHZ', 'AIA', 'AIB', 'AIC', 'AID', 'AIE', 'AIF', 'AIG', 'AIH', 'AII', 'AIK', 'AIL', 'AIM', 'AIN', 'AIO', 'AIP', 'AIR', 'AIS', 'AIT', 'AIU', 'AIV', 'AIW', 'AIX']
airportcodes = []
response = getResponse(airportcodes_url, headers)


if response.status_code == 200:
    data = response.json()
    # Process the data as needed
    # airportcodes.extend(extract_airport_codes(data))
    print(data)
else:
    print(f'Failed to fetch data: {response.status_code}, {response.text}')



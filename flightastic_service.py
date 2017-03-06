import json
from skyscanner.skyscanner import Flights

flights_service = Flights('prtl6749387986743898559646983194')
result = flights_service.get_result(
    country='IL',
    currency='USD',
    locale='en-GB',
    originplace='TLV-sky',
    destinationplace='NYCA-sky',
    outbounddate='2017-04-07',
    inbounddate='2017-04-13',
    stops=0,
    adults=2).parsed
    
# print(result)
trips = result['Itineraries']
# print trips[0]
# print trips[0]['PricingOptions'][0]['Price']
# smallest_prices =  [sorted(p['PricingOptions'], key=lambda k: k['Price'])[0] for p in trips]
# smallest_price = sorted(smallest_prices, key=lambda k: k['Price'])[0]
# print smallest_price
with open('output.json', 'w') as out:
    out.write(json.dumps(trips[0]))
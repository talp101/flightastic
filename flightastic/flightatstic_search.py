from skyscanner.skyscanner import Flights


class FlightasticSearch(object):

    FLIGHTS_SERVICE = Flights('prtl6749387986743898559646983194')

    def __init__(self, country='IL',
                 currency='USD',
                 locale='en-GB',
                 originplace='TLV-sky',
                 destinationplace='NYCA-sky',
                 outbounddate='2017-04-07',
                 inbounddate='2017-04-13',
                 stops=0,
                 adults=2):
        self._country = country
        self._currency = currency
        self._locale = locale
        self._originplace = originplace
        self._destinationplace = destinationplace
        self._outbounddate = outbounddate
        self._inbounddate = inbounddate
        self._stops = stops
        self._adults = adults

    def get_minimal_flight(self):
        result = self.FLIGHTS_SERVICE.get_result(country=self._country, currency=self._currency,
                                                 locale=self._locale, originplace=self._originplace,
                                                 destinationplace=self._destinationplace, outbounddate=self._outbounddate,
                                                 inbounddate=self._inbounddate, stops=self._stops, adults=self._adults).parsed
        return result['Itineraries'][0]
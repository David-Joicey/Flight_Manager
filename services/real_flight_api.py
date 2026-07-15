import requests
from flask import current_app

class RealFlightAPI:
    def __init__(self):
        # Gets API key from config and sets base URL for AviationStack API
        self.api_key = current_app.config.get('AVIATIONSTACK_API_KEY')
        self.base_url = 'http://api.aviationstack.com/v1/flights'

    def search_flights(self, origin, destination, date):
        #Checks if API key set
        if not self.api_key:
            raise ValueError("AviationStack API key not set")
        #Sets parameters for API request
        params = {
            'access_key': self.api_key,
            'dep_iata': origin,
            'arr_iata': destination,
            'flight_date': date
        }
        try:
            #Makes GET request to AviationStack API and raises exception for HTTP errors
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            #Normalises flight data
            raw_data = response.json().get('data', [])
            return self.normalise_flight_data(raw_data)
        
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error fetching flight data: {e}")
            return []
    
    def normalise_flight_data(self, raw_data):
        flights = []
        for flight in raw_data:
            try:
                #Normalises flight data to a consistent format
                flights.append({
                    'fnumber': flight.get('flight', {}).get('iata', 'N/A'),
                    'airline': flight.get('airline', {}).get('name', 'N/A'),
                    'origin': flight.get('departure', {}).get('iata', 'N/A'),
                    'destination': flight.get('arrival', {}).get('iata', 'N/A'),
                    'dtime': flight.get('departure', {}).get('estimated', 'N/A'),
                    'atime': flight.get('arrival', {}).get('estimated', 'N/A'),
                    'price': 100, #Placeholder
                    'date': flight.get('flight_date', 'N/A')
                })
            except Exception as e:
                current_app.logger.error(f"Error normalising flight data: {e}")
        return flights
"""
This module contains a real flight API service class used to get (real) live
flight data from the AviationStack API and display it to the user.
"""

import requests
from flask import current_app

class RealFlightAPI:
    """
    This service class is used to fetch the live flight data from the
    AviationStack API and format it into a suitable structure for the
    application. It also sets the api key from the environment variables/
    Flask configuration and gives the url to send requests to.
    """

    def __init__(self):
        # Gets API key from config and sets base URL for AviationStack API
        self.api_key = current_app.config.get('AVIATIONSTACK_API_KEY')
        self.base_url = 'https://api.aviationstack.com/v1/flights'

    def search_flights(self, origin, destination):
        """
        This method sends requests to the AviationStack /v1/flights route
        to get live flight data then normalises them using the normalise_flight_data
        method and either returns the received flights or raises an error.

        args:
            origin (str): Departure airport IATA code.
            destination (str): Arrival airport IATA code.
            date (str | None): Ignored for live flight data (AviationStack free tier).

        Returns:
            list[dict]: A list of normalised flight records. Returns an empty list
            if the API request fails or returns no usable data.

        Raises:
            ValueError: If the API key is missing.
        """

        #Checks if API key set
        if not self.api_key:
            raise ValueError("AviationStack API key not set")
        #Sets parameters for API request
        params = {
            'access_key': self.api_key,
            'dep_iata': origin,
            'arr_iata': destination,
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
        """
        Normalises flight data (if) received from the API request from the
        raw Json to a list of dictionaries format. The data normalised is the
        flight number (also icao or number), origin and destination from IATA codes,
        airline name as well as estimated departure and arrival times. Any data for fields
        that are not found for a flight are set to 'N/A' for consistency.

        args:
            raw_data (list[dict]): The 'data' list returned by the AviationStack API.
        
        Returns:
            list[dict]: A list of normalised flight dictionaries ready for use by
            templates and booking logic.
        """

        flights = []
        for flight in raw_data:
            try:
                #Normalises flight data to a consistent format
                flights.append({
                    'fnumber': (
                    flight.get('flight', {}).get('iata')
                    or flight.get('flight', {}).get('icao')
                    or flight.get('flight', {}).get('number')
                    or 'N/A'
                    ),
                    'airline': flight.get('airline', {}).get('name', 'N/A'),
                    'origin': flight.get('departure', {}).get('iata', 'N/A'),
                    'destination': flight.get('arrival', {}).get('iata', 'N/A'),
                    'dtime': flight.get('departure', {}).get('estimated', 'N/A'),
                    'atime': flight.get('arrival', {}).get('estimated', 'N/A'),
                })
            except Exception as e:
                current_app.logger.error(f"Error normalising flight data: {e}")
        return flights
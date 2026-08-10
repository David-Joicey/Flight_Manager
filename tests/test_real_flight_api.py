"""
This module contains testing for the real_flight_api AviationStack
API wrapper. It includes test cases for a successful API call,
missing API key and unsuccessful API call.
"""

import pytest
from unittest.mock import patch, MagicMock
from services.real_flight_api import RealFlightAPI
from flask import current_app

def test_search_flights(app):
    """
    This method tests for a successful API call using a mock response
    containing an example response from the AviationStack documentation
    edited to have project-relevant data in the required key-value pairs.

    Args:
        app: Flask application instance
    """

    mock_response = {
        #ALtered example response from AviationStack documentation
        "data": [
            {
                "flight_date": "2019-08-24",
                "flight_status": "scheduled",
                "departure": {
                    "airport": "string",
                    "timezone": "string",
                    "iata": "LHR",
                    "icao": "string",
                    "terminal": "string",
                    "gate": "string",
                    "delay": 0,
                    "scheduled": "2019-08-24T14:15:22Z",
                    "estimated": "2019-08-24T14:15:22Z",
                    "actual": "2019-08-24T14:15:22Z",
                    "estimated_runway": "2019-08-24T14:15:22Z",
                    "actual_runway": "2019-08-24T14:15:22Z",
                    "baggage": "string"
                },
                "arrival": {
                    "airport": "string",
                    "timezone": "string",
                    "iata": "CDG",
                    "icao": "string",
                    "terminal": "string",
                    "gate": "string",
                    "delay": 0,
                    "scheduled": "2019-08-24T14:15:22Z",
                    "estimated": "2019-08-24T14:15:22Z",
                    "actual": "2019-08-24T14:15:22Z",
                    "estimated_runway": "2019-08-24T14:15:22Z",
                    "actual_runway": "2019-08-24T14:15:22Z",
                    "baggage": "string"
                },
                "airline": {
                    "id": "string",
                    "fleet_average_age": 0,
                    "airline_id": "string",
                    "callsign": "string",
                    "hub_code": "string",
                    "iata_code": "string",
                    "icao_code": "string",
                    "country_iso2": "string",
                    "date_founded": "string",
                    "iata_prefix_accounting": "string",
                    "airline_name": "string",
                    "country_name": "string",
                    "fleet_size": 0,
                    "status": "string",
                    "type": "string"
                },
                "flight": {
                    "number": "string",
                    "iata": "BA249",
                    "icao": "string",
                    "codeshared": {}
                },
                "aircraft": {
                    "registration": "string",
                    "iata": "string",
                    "icao": "string",
                    "icao24": "string"
                }
            }
        ]   
    }

    with app.app_context():
        current_app.config['AVIATIONSTACK_API_KEY'] = 'testkey'

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response

            api = RealFlightAPI()
            flights = api.search_flights('LHR', 'JFK')

            assert flights[0]['fnumber'] == 'BA249'
            assert flights[0]['origin'] == 'LHR'
            assert flights[0]['destination'] == 'CDG'
            assert flights[0]['dtime'] == '2019-08-24T14:15:22Z'
            assert flights[0]['atime'] == '2019-08-24T14:15:22Z'

def test_no_api_key(app):
    """
    This method tests that creating an API wrapper class without an
    API key set as an environment variable results in a ValueError
    being raises

    Args:
        app: Flask application instance

    Raises:
        ValueError: If the API key is missing.
    """

    with app.app_context():
            current_app.config['AVIATIONSTACK_API_KEY'] = None
    
            api = RealFlightAPI()
            with pytest.raises(ValueError):
                 api.search_flights('LHR', 'JFK')

#Relevant API call error status codes
@pytest.mark.parametrize("status_code", [400, 401, 403, 404, 429, 500])
def test_search_flights_fail(app, status_code):
     """
     This method tests that an unsuccessful API call is handled correctly
     list by testing each relevant status code (400-500 for both client side
     and internal server errors) results in an empty flight list.

     Args:
        app: Flask application instance
        status_code: HTTP status codes for relevant API call related errors
     """
     
     with app.app_context():
             current_app.config['AVIATIONSTACK_API_KEY'] = 'testkey'
     
             with patch('requests.get') as mock_get:
                 mock_get.return_value.status_code = status_code
     
                 api = RealFlightAPI()
                 flights = api.search_flights('LHR', 'JFK')

                 assert flights == []
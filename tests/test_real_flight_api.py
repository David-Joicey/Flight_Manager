import pytest
from unittest.mock import patch, MagicMock
from services.real_flight_api import RealFlightAPI
from flask import current_app

def test_search_flights(app):
    mock_response = {
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
        current_app.config["AVIATIONSTACK_API_KEY"] = "testkey"

        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response

            api = RealFlightAPI()
            flights = api.search_flights("LHR", "JFK")

            assert flights[0]['fnumber'] == 'BA249'
            assert flights[0]['origin'] == 'LHR'
            assert flights[0]['destination'] == 'CDG'
            assert flights[0]['dtime'] == '2019-08-24T14:15:22Z'
            assert flights[0]['atime'] == '2019-08-24T14:15:22Z'
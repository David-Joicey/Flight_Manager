"""
This module contains tests for the MockFlightAPI class and its methods.
"""

from services.mock_flight_api import MockFlightAPI

test_api = MockFlightAPI()

def test_search_flights():
    """
    Tests the search_flights method from the MockFlightAPI class
    returns a valid list of generated flight data given the origin, destination and date.
    """

    origin = "LHR"
    destination = "CDG"
    date = "2026-10-15"

    flights = test_api.search_flights(origin, destination, date)

    assert isinstance(flights, list)
    assert len(flights) > 0

    for flight in flights:
        assert flight['origin'] == origin
        assert flight['destination'] == destination
        assert flight['date'] == date
        assert 'fnumber' in flight
        assert 'airline' in flight
        assert 'price' in flight
        assert 'dtime' in flight
        assert 'atime' in flight
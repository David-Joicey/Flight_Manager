import random
from datetime import datetime, timedelta, time

class MockFlightAPI:
    def __init__(self):
        self.flights = []

    def search_flights(self, origin, destination, date):
        # Mock airlines
        airlines = ['Ryanair', 'British Airways', 'Tui', 'EasyJet']

        #Generates randomised flights
        for i in range(random.randint(1, 10)):
            departure_time = time(random.randint(0, 23), random.randint(0, 59))
            arrival_time = time(random.randint(0, 23), random.randint(0, 59))
            airline = random.choice(airlines)

            flight = {
                'flight_number': f'{airline} {random.randint(100, 999)}',
                'airline': airline,
                'origin': origin,
                'destination': destination,
                'date': date,
                'price': random.randint(100, 500),
                'departure_time': departure_time,
                'arrival_time': arrival_time
            }
            self.flights.append(flight)
        return self.flights
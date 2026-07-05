import random
from datetime import datetime, timedelta, time

class MockFlightAPI:
    def __init__(self):
        self.flights = []

    def search_flights(self, origin, destination, date):
        #Clears previous search results
        self.flights = []
        # Mock airlines
        airlines = ['Ryanair', 'British Airways', 'Tui', 'EasyJet']

        #Generates randomised flights
        for i in range(random.randint(1, 10)):
            dtime = time(random.randint(0, 23), random.randint(0, 59))
            atime = time(random.randint(0, 23), random.randint(0, 59))
            airline = random.choice(airlines)

            flight = {
                'fnumber': f'{airline} {random.randint(100, 999)}',
                'airline': airline,
                'origin': origin,
                'destination': destination,
                'date': date,
                'price': random.randint(100, 500),
                'dtime': dtime,
                'atime': atime
            }
            self.flights.append(flight)
        return self.flights
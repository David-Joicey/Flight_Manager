# Flight-Manager

## Overview

Flight Manager is a full-stack flask-based web application project that provides the following features:
- Searching and booking of generated flights using a mock api
- List of (real) live flights providing departure and arival airports and esimated timings using the AviationStack free API plan
- Login + Sign up account authentication system
- Account-exclusive bookings and search history management

## Project Setup

### Virtual Environment

Terminal command to create the virtual environment:

`python -m venv .venv`

Terminal command to activate the virtual environment:

`.venv\Scripts\activate`

### Dependencies

Terminal command to install the required dependencies:

`pip install -r requirements.txt`

### API

Terminal command to set AviationStack API key (replace placeholder text in " " with key):

`$env:AVIATIONSTACK_API_KEY="api_key"`


### Flask

Terminal command to initialise the database:

`flask --app app init-db`

Terminal command to run the application:

`flask --app app run`

## Features

### Live Flights (API Integration)

The Live Flights feature uses the AviationStack API to show a list of live flights in a table including flight number, origin and destination airport IATA as well as estimated departure and arrival times. This feature can be accessed through the "live" route.

### Flight Booking (Using Mock API)

The Flight Booking feature allows users to enter flight details such as "From" and "To" airports and a departure date as well as a search button. If the form fields are all entered and search button pressed a table of (theoretical) flights are generated using a mock API. One of the table columns allows for the flights to be booked and added to the specific user's (account) bookings. These bookings can then be seen in the "bookings" route and cancelled/deleted.

### Authentication

### Database
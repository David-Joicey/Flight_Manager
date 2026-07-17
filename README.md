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

### Flight Booking (Using Mock API)

### Authentication

### Database

### UI (Jinja2 Templates)
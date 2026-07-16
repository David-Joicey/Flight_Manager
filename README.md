# Flight-Manager

## Overview

Flight Manager is a full-stack flask-based web application project that provides the following features:
- Searching and booking of generated flights using a mock api
- List of (real) live flights providing departure and arival airports and esimated timings
- Login + Sign up account authentication system
- Account-exclusive bookings and search history management

## Project Setup

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt


$env:AVIATIONSTACK_API_KEY="your_key_here"

flask --app app init-db
flask --app app run
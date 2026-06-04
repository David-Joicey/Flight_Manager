import os
from flask import Flask, render_template, request
from services.mock_flight_api import MockFlightAPI

#Factory Function to create Flask app instance
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'), #Change key in production
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    #Test configuration toggle
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    os.makedirs(app.instance_path, exist_ok=True)

    #Home page route
    @app.route('/')
    def home():
        return render_template('index.html')
    
    #Results page route
    @app.route('/results')
    def results():
        #Gets flight search parameters from the search form
        origin = request.args.get('From')
        destination = request.args.get('To')
        date = request.args.get('date')

        flights = MockFlightAPI().search_flights(origin, destination, date)
        return render_template('results.html', flights=flights, origin=origin, destination=destination, date=date)

    return app
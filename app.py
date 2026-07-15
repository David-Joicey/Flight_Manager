import os
from flask import Flask, current_app, flash, render_template, request
from database.db import get_db
from services.mock_flight_api import MockFlightAPI
from flask import g

from services.real_flight_api import RealFlightAPI

#Factory Function to create Flask app instance
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'), #Change key in production
        DATABASE=os.path.join(app.instance_path, 'database.sqlite'),
    )
    #Test configuration toggle
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    os.makedirs(app.instance_path, exist_ok=True)

    
    app.config['AVIATIONSTACK_API_KEY'] = os.getenv("AVIATIONSTACK_API_KEY")

    #Registers authentication blueprint
    from auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    #Registers search history blueprint
    from search_history import bp as search_history_bp
    app.register_blueprint(search_history_bp)

    #Registers booking blueprint
    from booking_list import bp as bookings_bp
    app.register_blueprint(bookings_bp)

    #Initialises database
    from database import db
    db.init_app(app)

    from auth import login_required

    #Home page route
    @app.route('/')
    @login_required
    def home():
        return render_template('index.html')
    
    #Results page route
    @app.route('/results')
    @login_required
    def results():
        #Gets flight search parameters from the search form
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        date = request.args.get('date')

        #Saves search to database
        if origin and destination and date:
            database = get_db()
            try:
                database.execute(
                    'INSERT INTO SearchHistory (uid, origin, destination, date) VALUES (?, ?, ?, ?)',
                    (g.user['uid'], origin, destination, date)
                )
                database.commit()
            except Exception as e:
                database.rollback()
                flash('Error occurred while saving search history.')

        api = MockFlightAPI()
        flights = api.search_flights(origin, destination, date)

        return render_template('results.html', flights=flights, origin=origin, destination=destination, date=date)

    print("DB FILE:", app.config["DATABASE"])

    return app
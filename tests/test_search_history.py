"""
This module contains tests for the search _history route and its methods.
"""

from database.db import get_db
from app import create_app
from datetime import date

def test_search_history(auth_client, app):
    """
    This method tests that the a flight search results in a corresponding row
    being inserted into the SearchHistory table with correct data by sending a
    get request to the results route with flight data.

    Args:
        auth_client: Flask test client instance with a registered and logged-in user.
        app: Flask application instance
    """

    response = auth_client.get('/results', 
                                query_string={'origin': 'JFK', 'destination': 'LAX', 'date': '2024-06-01'}, follow_redirects=True
                                )

    assert response.status_code == 200

    with app.app_context():
        db = get_db()
        history = db.execute(
            'SELECT origin, destination, date FROM SearchHistory WHERE uid = ?', (1,)
        ).fetchone()

        assert history is not None
        assert history['origin'] == 'JFK'
        assert history['destination'] == 'LAX'
        assert history['date'] == date(2024,6,1)
        
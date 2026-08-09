"""
This module contains test cases for the bookings route for checking
valid booking data insert into the database and successful booking
cancellation (deletion from database).
"""

from database.db import get_db
from app import create_app
from datetime import date

def test_bookings(auth_client, app):
    """
    This method tests that the bookings route correctly displays booking information
    from the Bookings database table by inserting a booking record into the db and
    querying it then checking the flight data is valid. Uses a logged-in test client to
    make sure bookings route is reachable.

    Args:
        auth_client: Flask test client instance with a registered and logged-in user.
        app: Flask application instance
    """

    with app.app_context():
        db = get_db()
        #Insert booking
        db.execute(
            """
            INSERT INTO Bookings (uid, fnumber, airline, price, origin, destination, atime, dtime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                'BA123',
                'British Airways',
                150,
                'LHR',
                'CDG',
                '13:00',
                '14:00'
            ),
        )
        db.commit()

        booking = db.execute(
            """
            SELECT fnumber, airline, price, origin, destination, atime, dtime
            FROM Bookings WHERE uid = ?
            """, (1,)
        ).fetchone()

        response = auth_client.get('/bookings', follow_redirects = True)
        assert response.status_code == 200

        #DB columns
        assert booking['fnumber'] == 'BA123'
        assert booking['airline'] == 'British Airways'
        assert booking['price'] == 150
        assert booking['origin'] == 'LHR'
        assert booking['destination'] == 'CDG'
        assert booking['atime'] == '13:00'
        assert booking['dtime'] == '14:00'

def test_booking_cancel(auth_client, app):
    """
    This method tests that a booking is successfully cancelled/deleted
    by the inserting booking information and passing the booking id (bid)
    into the cancel/bid endpoint.

    Args:
        auth_client: Flask test client instance with a registered and logged-in user.
        app: Flask application instance
    """

    with app.app_context():
        db = get_db()
        #Save bid for use in cancel route
        bid = 1
        #Inserts booking
        db.execute(
            """
            INSERT INTO Bookings (uid, fnumber, airline, price, origin, destination, atime, dtime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                bid,
                "BA123",
                "British Airways",
                150,
                "LHR",
                "CDG",
                "13:00",
                "14:00",
            ),
        )
        db.commit()

        response = auth_client.post(f"/bookings/cancel/{bid}", follow_redirects=True)

        assert response.status_code == 200

        #Verify Deletion
        with app.app_context():
            db = get_db()
            deleted = db.execute(
                "SELECT * FROM Bookings WHERE bid = ?", (bid,)
            ).fetchone()

            assert deleted is None
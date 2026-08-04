"""
Module for test fixtures and setup for the Flask application instance used in testing.
Uses pytest fixtures to create a temporary database and configure the app for testing.
"""

import pytest
import os
import tempfile
from app import create_app
from database.db import init_db, get_db

@pytest.fixture
def app():
    """
    Creates a Flask application instance for testing.
    Initialises a temporary database with identical schema to production database.
    """
    # Create a temporary file to use as the test database
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'AVIATIONSTACK_API_KEY': os.getenv("AVIATIONSTACK_API_KEY", "test_api_key")
    })

    with app.app_context():
        get_db().executescript(
            """
            CREATE TABLE Users (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(15) NOT NULL UNIQUE,
                phash VARCHAR(255) NOT NULL
            );
            CREATE TABLE SearchHistory (
                sid INTEGER PRIMARY KEY AUTOINCREMENT,
                uid INTEGER NOT NULL,
                origin VARCHAR(100) NOT NULL,
                destination VARCHAR(100) NOT NULL,
                date DATE NOT NULL,
                FOREIGN KEY (uid) REFERENCES Users(uid)
            );
            CREATE TABLE Bookings (
                bid INTEGER PRIMARY KEY AUTOINCREMENT,
                uid INTEGER NOT NULL,
                fnumber VARCHAR(10) NOT NULL,
                airline VARCHAR(100) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                origin VARCHAR(100) NOT NULL,
                destination VARCHAR(100) NOT NULL,
                atime VARCHAR(10) NOT NULL,
                dtime VARCHAR(10) NOT NULL,
                FOREIGN KEY (uid) REFERENCES Users(uid)
            );
            """

        )

    yield app

    # Close and remove the temporary database file after tests
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """
    Creates a test client for the Flask application instance.
    Allows sending HTTP requests to the app during testing.

    Returns:
        Flask test client instance
    """
    return app.test_client()

@pytest.fixture
def runner(app):
    """
    Creates a test runner for Flask CLI commands

    Returns:
        Flask test CLI runner instance
    """
    return app.test_cli_runner()

@pytest.fixture
def auth_client(client):
    """
    Creates a registered and logged-in test client for the test instance.

    Returns:
        Flask test client instance with a registered and logged-in user.
    """

    client.post('/auth/register', data={'username': 'testuser', 'password': 'testpass'})
    client.post('/auth/login', data={'username': 'testuser', 'password': 'testpass'})
    return client

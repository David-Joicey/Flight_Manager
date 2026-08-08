"""
This module contains tests for the authentication blueprint.
Checks that registration page renders correctly, directs to login
after a successful registration and tests registration input validation
"""

import pytest
from flask import g, session
from database.db import get_db
from werkzeug.security import generate_password_hash

def test_register(client, app):
    """
    Tests registration page renders and directs to login page after successful registration.
    Also checks that the new user is added to the database after registration.

    Args:
        client: Flask test client instance
        app: Flask application instance
    """

    assert client.get("/auth/register").status_code == 200
    response = client.post(
        "/auth/register", data={"username": "ExampleUsername", "password": "ExamplePassword"}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        db = get_db()
        assert (
            db.execute(
                "SELECT * FROM Users WHERE username = 'ExampleUsername'"
                ).fetchone() is not None
        )

@pytest.mark.parametrize(
    ("username", "password"),
    (
        ("", ""),
        ("abcdefg", ""),
        ("ab", "password"),
        ("testusernametoolongmorethan20chars", "password"),
        ("abcdefg", "short"),
        ("abcdefg", "toolongpasswordthatexceeds20characters"),
        ("testuser", "testpass"),
    )
)

def test_register_input_validation(client, username, password, app):
    """
    Tests registration input validation using invalid registration data
    by making sure each set of data used keeps the user on the registration page.

    client: Flask test client instance
    app: Flask application instance
    username: string being passed in as the username
    password: string being passed in as the password
    """

    #Creates a test user to check for duplicate username validation
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO Users (username, phash) VALUES (?, ?)",
            ("testuser", generate_password_hash("testpass"))
        )
        db.commit()

    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    #Code 200 shows still on registration page, invalid input not worked
    assert response.status_code == 200

def test_login(client, auth_client):
    """
    Tests the login page renders and directs user to the home route
    and checks that the logged in client has the correct user data.

    Args:
    client: Flask test client instance
    auth_client: Flask test client instance with a registered and logged-in user.
    """

    assert client.get("/auth/login").status_code == 200

    #Logs in test user
    response = auth_client.post(
        "/auth/login", data={"username": "testuser", "password": "testpass"}
    )
    assert response.headers["Location"] == "/"

    #Checks logged in user data
    with auth_client:
        auth_client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "testuser"

@pytest.mark.parametrize(
    ("username", "password"),
        (
            ("", ""),
            ("abcdefg", ""),
            ("ab", "password"),
            ("testusernametoolongmorethan20chars", "password"),
            ("abcdefg", "short"),
            ("abcdefg", "toolongpasswordthatexceeds20characters"),
        )
    )
def test_login_input_validation(client, username, password):
    """
    Tests login input validation using invalid login data
    by making sure each set of data used keeps the user on the login page.

    Args:
        client: Flask test client instance
        username: Username string to test login input validation
        password: Password string to test login input validation
    """

    response = client.post(
        "/auth/login", data={"username": username, "password": password}
    )
    #Code 200 shows still on login page, invalid input not worked
    assert response.status_code == 200

def test_logout(auth_client):
    """
    Tests logout functionality by logging out a logged-in user
    and checking their user-id is removed from the session as
    well as thr response code showing a redirect.

    Args:
        auth_client: Flask test client instance with a registered and logged-in user.
    """

    response = auth_client.get("/auth/logout")
    with auth_client:
        auth_client.get("/")
        assert "user_id" not in session
    assert response.status_code in (302, 308)
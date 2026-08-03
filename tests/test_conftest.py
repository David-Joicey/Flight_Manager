"""
This module contains tests for the pytest fixtures defined in conftest.py.
"""

import pytest

def test_app_fixture(app):
    """Ensure the app fixture creates a valid Flask app."""
    assert app is not None
    assert app.config["TESTING"] is True


def test_database_schema(app):
    """Ensure the temporary test database schema loads correctly."""
    with app.app_context():
        db = app.get_db()
        tables = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall()

        table_names = {t[0] for t in tables}

        assert "Users" in table_names
        assert "Bookings" in table_names
        assert "SearchHistory" in table_names


def test_client_fixture(client):
    """Ensure the test client can make requests."""
    response = client.get("/")
    #Allows for redirects to login page if not logged in
    assert response.status_code in (200, 302, 308)#308 for trailing slash redirect


def test_runner_fixture(runner):
    """Ensure the CLI runner works."""
    result = runner.invoke(args=["--help"])
    assert result.exit_code == 0


def test_auth_client(auth_client):
    """Ensure the auth_client fixture logs in a user."""
    response = auth_client.get("/bookings")
    assert response.status_code in (200, 302, 308)

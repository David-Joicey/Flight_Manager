"""
Module containing tests for database connection, initialisation
and schema.
Uses the temporary database created in conftest.py that mirrors the production schema.
"""

import sqlite3
import pytest
from database.db import get_db

def test_get_and_close_db(app):
    """
    Test the get_db() function by checking it returns the same connection
    and that the connection closes properly.

    Args:
        app: Test flask application instance
    """

    #get section
    with app.app_context():
        db = get_db()
        #The same connection should be returned
        assert db is get_db()

    #close section
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    """
    Tests that the init-db command calls init_db() to initialise the database
    and outputs the expected message.

    Args:
        runner: Flask test CLI runner instance
        monkeypatch: Pytest fixture to modify init_db() safely for testing
    """

    class Recorder:
        called = False
    def fake_init_db():
        Recorder.called = True
    
    monkeypatch.setattr('database.db.init_db', fake_init_db)

    result = runner.invoke(args=['init-db'])

    assert 'Initialised database' in result.output
    assert Recorder.called

def test_db_schema(app):
    """
    Tests that the database schema contains the expected tables: Users, SearchHistory, and Bookings.

    Args:
        app: Test flask application instance
    """

    with app.app_context():
        db = get_db()
        #Database metadata held in sqlite_master table (for table names)
        tables = db.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

        #Set comprenhension for table names (O(1)) to avoid searching tuples
        table_names = {table['name'] for table in tables}

        assert 'Users' in table_names
        assert 'SearchHistory' in table_names
        assert 'Bookings' in table_names

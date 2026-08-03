"""
This module contains test cases for the factory function in app.py.
"""
import os
from app import create_app

def test_config():
    """
    Tests that the Flask application instance is created with the indended configuration
    for production or testing.
    """
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

"""
This module contains configuration settings for the application,
which is the API key for the AviationStack API used to fetch live flight data.
It is loaded from environment variables to keep api keys hidden and secure.
"""

import os

AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
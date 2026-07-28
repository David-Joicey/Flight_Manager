"""
This module contains the search history route for the application.
It allows for user-specific search history to be displayed for the currently logged-in user.
"""

from flask import (
    Blueprint, flash, g, render_template, request, session, url_for
)
from database.db import get_db
from auth import login_required

#Blueprint for search history routes
bp = Blueprint('search_history', __name__, url_prefix='/search_history')

#Search history route
@bp.route('/')
@login_required
def search_history():
    """
    Displays the search history for the currently logged-in user.
    Queries the database for search history records with matching user ID (uid)
    to the logged-in user and orders them by date (descending).
    Requires user to be logged in to access.

    Returns:
        Rendered HTML Jinja2 template "search_history.html" with the user's search history.
    """

    db = get_db()
    #Gets history by user id of logged in user
    searches = db.execute(
        'SELECT origin, destination, date '
        'FROM SearchHistory WHERE uid = ? ORDER BY date DESC',
        (g.user['uid'],)
    ).fetchall()

    return render_template('search_history.html', searches=searches)
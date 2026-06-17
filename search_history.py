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
    db = get_db()
    #Gets history by user id of logged in user
    searches = db.execute(
        'SELECT origin, destination, date '
        'FROM SearchHistory WHERE uid = ? ORDER BY date DESC',
        (g.user['uid'],)
    ).fetchall()

    return render_template('search_history.html', searches=searches)
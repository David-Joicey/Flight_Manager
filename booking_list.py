from flask import (
    Blueprint, flash, g, render_template, request, session, url_for
)
from database.db import get_db
from auth import login_required

#Blueprint for booking routes
bp = Blueprint('bookings', __name__, url_prefix='/bookings')

#Booking route
@bp.route('/')
@login_required
def bookings():
    db = get_db()
    #Gets booking history by user id of logged in user
    bookings = db.execute(
        'SELECT fnumber, airline, price, origin, destination, atime, dtime '
        'FROM Bookings WHERE uid = ? ORDER BY dtime DESC',
        (g.user['uid'],)
    ).fetchall()

    return render_template('booking_list.html', bookings=bookings)
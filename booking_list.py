from flask import (
    Blueprint, flash, g, render_template, request, session, url_for, redirect
)
from database.db import get_db
from auth import login_required

#Blueprint for booking routes
bp = Blueprint('bookings', __name__, url_prefix='/bookings')

#Booking list route
@bp.route('/')
@login_required
def bookings():
    db = get_db()
    #Gets booking history by user id of logged in user
    bookings = db.execute(
        'SELECT * '
        'FROM Bookings WHERE uid = ? ORDER BY dtime DESC',
        (g.user['uid'],)
    ).fetchall()

    return render_template('booking_list.html', bookings=bookings)

#Route adds a booking to the database
@bp.route('/book', methods=['POST'])
@login_required
def book():
    fnumber = request.form['fnumber']
    airline = request.form['airline']
    price = request.form['price']
    origin = request.form['origin']
    destination = request.form['destination']
    atime = request.form['atime']
    dtime = request.form['dtime']

    db = get_db()
    #Inserts booking into database
    try:
        db.execute(
            'INSERT INTO Bookings (uid, fnumber, airline, price, origin, destination, atime, dtime) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (g.user['uid'], fnumber, airline, price, origin, destination, atime, dtime)
        )
        db.commit()
        flash('Booking successful!')
    except Exception as e:
        db.rollback()
        flash('Error occurred while adding booking.')

    return redirect(url_for('bookings.bookings'))

#Route removes a booking from the database
@bp.route('/cancel/<int:bid>', methods=['POST'])
@login_required
def cancel(bid):
    db = get_db()
    #Deletes booking from database
    try:
        db.execute(
            'DELETE FROM Bookings WHERE bid = ? AND uid = ?',
            (bid, g.user['uid'])
        )
        db.commit()
        flash('Booking canceled')
    except Exception as e:
        db.rollback()
        flash('Error occurred while canceling booking.')
    return redirect(url_for('bookings.bookings'))
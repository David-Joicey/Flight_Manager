"""
Module for user authentication routes and functions in the Flask application.
Includes user registration, login, logout, and session management.
Provides a decorator to require login for certain views.
"""

import os
print("AUTH FILE LOADED FROM:", os.path.abspath(__file__))
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash#
from database.db import get_db

#Blueprint for authentication routes
bp = Blueprint('auth', __name__, url_prefix='/auth')

#Decorator to require being logged in for certain views
def login_required(view):
    """
    Decorator method used as a modifier for routes that require the user to be logged in.
    If the user is not logged in, they will be redirected to the login page.

    args:
        view (function): The view function to be wrapped by the decorator.

    returns:
        function: The wrapped view function that checks for user login status.
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):

        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """
    Method loads the logged-in user's information from the database before each request.
    If the user is logged in, their information is stored in the `g` object for
    easy access throughout the application. If the user is not logged in, `g.user` is set to None.
    """

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM Users WHERE uid = ?', (user_id,)
        ).fetchone()

#Registers new users
@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Registers a new user with the user provided username and password from the registration form.
    Checks for existing users with the same username and validates the input data to make sure
    within the required length and fields are not empty.
    If the registration is successful, the user is redirected to the login page. If there are any errors,
    the user is shown an error message and remains on the registration page.
    Adds the new user data to the database if there are no errors.
    Passwords are hashed before being stored in the database for security.
    """

    #Handles and validates registration form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username required.'
        elif not password:
            error = 'Password required.'
        
        elif len(password) < 8 or len(password) > 20:
            error = 'Password must be between 8 and 20 characters long.'
        elif len(username) < 4 or len(username) > 20:
            error = 'Username must be between 4 and 20 characters long.'

        #Checks if user with same username already exists in the database
        elif db.execute(
            'SELECT uid FROM Users WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        #Adds new user data to database if no errors
        if error is None:
            try:
                db.execute(
                    'INSERT INTO Users (username, phash) VALUES (?, ?)',
                    (username, generate_password_hash(password))
                )
                db.commit()
            except Exception as e:
                db.rollback()
                flash('Error occurred while registering new user.')
            #Redirects to login page after successful registration
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')

#Logs in existing users
@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Logs in an existing user with the provided username and password from the login form.
    Validates input data to ensure they are within the required lengths.
    If the login is successful, the user's ID is stored in the session and they are redirected
    to the home page. If there are any errors, the user is shown an error message and remains on the login page.
    """

    #Handles and validates login form
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(password) < 8 or len(password) > 20:
            flash('Password must be between 8 and 20 characters long.')
            return render_template('auth/login.html')
        
        elif len(username) < 4 or len(username) > 20:
            flash('Username must be between 4 and 20 characters long.')
            return render_template('auth/login.html')

        db = get_db()
        error = None
        #Gets given data from database if it exists in database
        user = db.execute(
            'SELECT * FROM Users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        #Checks if password is correct by comparing hashes
        elif not check_password_hash(user['phash'], password):
            error = 'Incorrect password.'

        #Logs in user by storing their id in the session if no errors
        if error is None:
            session.clear()
            session['user_id'] = user['uid']
            return redirect(url_for('home'))

        flash(error)
    return render_template('auth/login.html')

#Logs out users by clearing the session
@bp.route('/logout')
def logout():
    """
    Logs out the currently logged-in user by clearing the session data.
    After logging out, the user is redirected to the home page.
    """

    session.clear()
    return redirect(url_for('home'))
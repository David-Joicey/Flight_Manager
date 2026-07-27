"""
This module is used for interacting with the SQLite database.
It contains methods for connecting to, closing and initialising the database
as well as defining a CLI command for initialising the database.
"""

import sqlite3
from datetime import datetime
import click
from flask import current_app, g

#Database connection
def get_db():
    """
    Method connects to the SQLite database if not already connected by checking if 'db' is in the 
    Flask application context global object 'g'.

    returns:
        SQLite database connection object
    """
    
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            #Converts SQLite types to Python types
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

#Closes database connection
def close_db(e=None):
    """
    Method closes the SQLite database connection if it exists in the
    Flask application context global object 'g'.

    args:
        e (Exception/None): Optional exception object. Defaults to None.
    """

    db = g.pop('db', None)
    if db is not None:
        db.close()

#Initialises database
def init_db():
    """
    Method initialises the SQLite database by executing the SQL commands in the 'schema.sql' file.
    It connects to the database using the get_db() method and executes the explained SQL commands
    to create the necessary tables and schema for the application.
    """

    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


#CLI to initialise database
@click.command('init-db')
def init_db_command():
    """
    Method defines a command-line interface (CLI) command 'init-db'
    that can be used to initialise the SQLite database by calling the init_db() method.
    It uses the click library to define the command and provides feedback to the user
    by printing a message 'Initialised database' to the console after the database has been initialised.
    """

    init_db()
    click.echo('Initialised database')

#Connects database functions to Flask app
def init_app(app):
    """
    Method connects the database functions to the Flask application instance.
    It registers the close_db() method to be called when the application context is torn down,
    and adds the init_db_command() method as a CLI command.

    args:
        app (Flask): Flask application instance
    """

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
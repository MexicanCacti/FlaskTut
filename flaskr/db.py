import sqlite3

import click #Creates CLI interfaces
from flask import current_app #import flask app handling current request
from flask import g

def get_db():   # gets database connection
    if 'db' not in g:   # checks if database connection doesn't exist
        g.db = sqlite3.connect( # create db connection & store in g
            current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES
            #current_app.config['DATABASE']: retrieves datavase path from Flask config
            #detect_types=sqlite3.PARSE_DECLTYPES: Enable type connection for SQLite
        )
        g.db.row_factory = sqlite3.Row # allow named access for columns

    return g.db

def close_db(e=None): #closes database connection
    db = g.pop('db', None) #Attempt to remove & return db conn from g
    if db is not None: #check if db conn found
        db.close() # closes


def init_db():  #init database
    db = get_db()   #gets db connection

    with current_app.open_resource('schema.sql') as f: # opens scheme.sql file
        db.executescript(f.read().decode('utf8')) #Execute SQL script to init database schema


@click.command('init-db') #Click command named init-db
def init_db_command():  
    init_db()   #calls function to init database
    click.echo('Inited the database.') #msg to cli

def init_app(app):
    app.teardown_appcontext(close_db) #regs close_db func to be called when app context torn down (ensures db closes)
    app.cli.add_command(init_db_command) #adds init_db_command to Flask CLI commands
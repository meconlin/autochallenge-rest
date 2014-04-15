import logging
import sqlite3
import json
import os

from flask import Flask, jsonify, request, g
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

path = os.path.dirname(os.path.abspath(__file__))
DATABASE = '%s/database.db'%path

def get_db():
    """
    get a connection
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """
    open local schema.sql file and create data model
    you can run me from the command line using
    >>>> from word import init_db()
    >>>> init_db()
    """
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    """
    run a query
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    print rv
    return (rv[0] if rv else None) if one else rv

def clear_db():
    """
    truncate table
    """
    cur = get_db().execute("delete from words")
    cur.close()

def upsert_db(word):
    """
    try to insert, if it fails ignore it (existing)
    update count to count+1 
    """
    app.logger.error("upsert called with : %s"%word)
    cur = get_db()
    cur.execute("insert or ignore into words values (?,?)", (word, 0,) )
    cur.commit()
    cur.execute("update words set count=count+1 where word=?", (word,))
    cur.commit()
    cur.close()

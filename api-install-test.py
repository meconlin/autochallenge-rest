import logging
import json
from words import get_db, query_db, clear_db, upsert_db

from flask import Flask, jsonify, request
from logging.handlers import RotatingFileHandler

app = Flask(__name__)



if __name__ == "__main__":
   print "I started and could have done something"

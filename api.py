import logging
import json
from words import get_db, query_db, clear_db, upsert_db

from flask import Flask, jsonify, request
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

def word_validate(word):
    """
    check that word is a single word
    """
    if(word.split()[-1] == word): 
        return True

    return False

@app.route("/word/<wordname>", methods=['GET', 'PUT'])
def word(wordname):
    """
    PUT - add word to datastore, increment count if update
    GET - return word and count
    """
    try:
        if request.method == 'PUT':
            data = request.get_json(force=True)
            
            if word_validate(data['word']):
                if data['word']:
                    upsert_db(data['word'])

                return jsonify({'okay':'true'}), 201
            else:
                return jsonify({ "error": "PUT requests must be one word in length" })

        elif request.method == 'GET':
            word_db = query_db('select * from words where word = ?',(wordname,), True)
            if word_db:
                return jsonify({word_db[0]:word_db[1]})
        else:
            abort(403)
    except Exception, e:
        app.logger.error('Error ! : %s'%e)
        abort(404)

    return jsonify({})

@app.route("/words", methods=['GET'])
def words():
    """
    return list of words and their count from the datastore
    blank if none found
    """
    foundwords = {}
    try:
        for word in query_db('select * from words'):
            foundwords[word[0]] = word[1]
    except Exception, e:
        app.logger.error('Error ! : %s'%e)
        abort(404)

    return jsonify(foundwords)

@app.route("/")
def home():
    """
    Home - return api doco
    """
    api = {
        "/words":"GET - List of words and their counts",
        "/word/<wordname>":"GET/PUT - Create a word and init its count to 1. or list count for a word"
    }
    return jsonify(api)

def init_loggers():
    handler = RotatingFileHandler('flask_toy.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    
    chandler = logging.StreamHandler()
    chandler.setLevel(logging.DEBUG)  

    app.logger.addHandler(handler)
    app.logger.addHandler(chandler)


if __name__ == "__main__":
    init_loggers()
    app.run()
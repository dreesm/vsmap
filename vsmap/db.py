from flask import g
from pymongo import MongoClient
import urllib
import json
from bson.objectid import ObjectId

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return obj

def get_db():
    if 'db' not in g:
        if 'dbusr' not in g:
            usr = 'vsmap'
        if 'dbpwd' not in g:
            pwd = 'vsmap'
        if 'dbauth' not in g:
            authdb = 'vsmap'
        dbsite = '127.0.0.1:27017'
        dbauthmechanism = 'SCRAM-SHA-256'
        uri = 'mongodb://%s:%s@%s/%s' % (urllib.parse.quote_plus(usr), urllib.parse.quote_plus(pwd), dbsite, authdb)
        client = MongoClient(uri)
        g.client = client
        g.db = g.client.vsmap
    
    return g.client

def close_db(e=None):
    client = g.pop('client', None)

    if client is not None:
        db = g.pop('db', None)
        client.close()

def init_app(app):
    app.teardown_appcontext(close_db)
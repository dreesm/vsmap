from flask import g
from pymongo import MongoClient
import urllib

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
        url = 'mongodb://%s:%s@%s/authSource=%s&authMechanism=%s' % (urllib.parse.quote_plus(usr), urllib.parse.quote_plus(pwd), dbsite, authdb, dbauthmechanism)
        client = Mongoclient(url)
        g.client = client
        g.db = g.client.vsmap
    
    return g.client

def close_db():
    client = g.pop('client', None)

    if client is not None:
        db = g.db.pop('db', None)
        client.close()

def init_app(app):
    app.teardown_appcontext(close_db)
from flask import Flask, render_template
from . import db

def create_app():
    app = Flask(__name__)
    db.init_app(app)

    @app.route('/')
    def index():
        cursor = db.get_db()
        streams = []
        for doc in cursor.vsmap.valuestreams.find():
            streams.append = doc['name']
        
        if request.method == 'POST':
            vsname = request.form['vsname']
            if not vsname:
                error = 'Value stream name is required'


        return render_template('index.html', streams=streams)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

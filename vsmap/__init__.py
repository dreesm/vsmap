from flask import Flask
from . import db

def create_app():
    app = Flask(__name__)
    db.init_app(app)

    @app.route('/')
    def index():
        cursor = db.get_db()
        exist  = cursor.workcenter.find_one()
        if exist is None:
            return 'No data in db'
        else:
            return 'data in db'

    @app.route('/hello')
    def hello():
        return 'Hello, World'

    return app

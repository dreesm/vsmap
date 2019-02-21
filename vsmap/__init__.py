from flask import (
    Flask, render_template, redirect, request, url_for, flash
)

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    from . import db
    from . import streams
    db.init_app(app)
    app.register_blueprint(streams.bp)

    @app.route('/', methods=('GET', 'POST'))
    def index():
        error = None
        cursor = db.get_db()
        streams = []
        unclearstreams = []
        for doc in cursor.vsmap.valuestreams.find():
            try:
                streams.append(doc['vsname'])
            except KeyError:
                unclearstreams.append(doc)
        
        if request.method == 'POST':
            vsname = request.form['vsname']
            new = request.form['new']
            if not vsname:
                error = 'Value stream name is required'
            elif new and vsname in streams:
                error = 'Value stream name is already taken'
            
            if error is None:
                if new:
                    cursor.vsmap.valuestreams.insert_one({'vsname': vsname})
                return redirect(url_for('streams.overview', stream=vsname))
            
            flash(error)

        return render_template('index.html', streams=streams)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

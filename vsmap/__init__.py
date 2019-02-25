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
    from . import parts
    from . import polishtraveler
    db.init_app(app)
    app.register_blueprint(streams.bp)
    app.register_blueprint(parts.bp)
    app.register_blueprint(polishtraveler.bp)

    @app.route('/', methods=('GET', 'POST'))
    def index():
        error = None
        cursor = db.get_db()
        streams = []
        unclearstreams = []
        parts = []
        unclearparts = []
        for doc in cursor.vsmap.valuestreams.find():
            try:
                if doc['vsname'] not in streams:
                    streams.append(doc['vsname'])
            except KeyError:
                unclearstreams.append(doc)
        for doc in cursor.vsmap.parts.find():
            try:
                if doc['partname'] not in parts:
                    parts.append(doc['partname'])
            except KeyError:
                unclearparts.append(doc)
        
        if request.method == 'POST':
            formnum = request.form['form']
            if formnum == "1":
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

            if formnum == "2":
                part = request.form['partname']
                return redirect(url_for('parts.overview', part=part))
            flash(error)

        return render_template('index.html', streams=streams, parts=parts)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

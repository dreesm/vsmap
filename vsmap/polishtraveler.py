from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from . import db

bp = Blueprint('polish', __name__, url_prefix='/polish')


@bp.route('/', methods=('GET', 'POST'))
def index():
    error = None
    cursor = db.get_db()
    workOrders = []
    unclearWorkOrders = []
    for doc in cursor.vsmap.polish.find():
        try:
            workOrders.append(doc['WONUM'])
        except KeyError:
            unclearstreams.append(doc)

    if request.method == 'POST':
        formnum = request.form['form']
        if formnum == "1":
            WONUM = request.form['WONUM']
            new = request.form['new']
            if not WONUM:
                error = 'Work Order number is required'
            elif new and WONUM in workOrders:
                error = 'Work Order number is already in use'
            
            if error is None:
                if new:
                    cursor.vsmap.polish.insert_one({'WONUM': WONUM})
                return redirect(url_for('polish.overview', WO=WONUM))

    return render_template('polish/index.html', workOrders=workOrders)


@bp.route('/<WO>/', methods=('GET', 'POST'))
def overview(WO):
    error = None
    cursor = db.get_db()
    polishdict = cursor.vsmap.polish.find_one({'WONUM': WO})
    try:
        types = polishdict['types']
    except KeyError:
        types = []
    try:
        sides = polishdict['sides']
    except KeyError:
        sides = []
    
    if request.method == 'POST':
        formnum = request.form['form']
        if formnum == "1":
            side = request.form['side']
            new = request.form['new']

    


    return render_template('polish/WO.html', WO=WO, types=types, sides=sides)
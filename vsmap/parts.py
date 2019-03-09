from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session
)
from . import db
from bson.objectid import ObjectId

bp = Blueprint('parts', __name__, url_prefix='/part')

@bp.route('/<part>/overview', methods=('GET', 'POST'))
def overview(part):
    cursor = db.get_db()
    testpartname = None
    testpartdict = cursor.vsmap.parts.find_one({'_id': ObjectId(session['partid'])})
    testpartname = testpartdict['partname']
    if testpartname == None:
        testpartname = 'error'
    return render_template('parteditor/overview.html', part=part, testpart=testpartname)
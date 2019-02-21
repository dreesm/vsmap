from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from . import db

bp = Blueprint('streams', __name__, url_prefix='/valuestreams')

@bp.route('/<stream>/overview', methods=('GET', 'POST'))
def overview(stream):
    cursor = db.get_db()
    streamdict = cursor.vsmap.valuestreams.find_one({'vsname': stream})
    partlist = []
    if 'parts' in streamdict:
        for part in streamdict['parts']:
            partlist.append(streamdict['parts'][part]['name'])
    else:
        partlist.append('no parts in value stream')

    if request.method == 'POST':
        newpart = request.form['newpart']
        if not newpart:
            error = "part name is required"
        
        if 'parts' in streamdict:
            streamdict['parts'][newpart] = {'name': newpart}
        else:
            streamdict['parts'] = {newpart: {'name': newpart}}
        
        flash(error)

        if error is None:
            cursor.vsmap.valuestreams.replace_one({'_id':streamdict['_id']}, streamdict)
            return redirect(url_for('streams.overview', stream=stream))

    return render_template('vseditor/overview.html', stream=stream, partlist=partlist)
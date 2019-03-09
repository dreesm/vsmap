from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session
)
from . import db
import json

bp = Blueprint('streams', __name__, url_prefix='/valuestreams')

@bp.route('/<stream>/overview', methods=('GET', 'POST'))
def overview(stream):
    cursor = db.get_db()
    streamdict = cursor.vsmap.valuestreams.find_one({'vsname': stream})
    partlist = []
    nopartlist = []
    if 'parts' in streamdict:
        for part in streamdict['parts']:
            partlist.append(streamdict['parts'][part]['name'])
    else:
        nopartlist.append('No parts have been added to value stream')

    if request.method == 'POST':
        formnum = request.form['form']
        error = None
        if formnum == "1":
            partchange = request.form['change']
            part = request.form['part']
            if partchange == 'Remove':
                streamdict['parts'].pop(part, None)
                cursor.vsmap.valuestreams.replace_one({'_id':streamdict['_id']}, streamdict) 
                return redirect(url_for('streams.overview', stream=stream))
            elif partchange == 'Edit':
                if 'partid' in streamdict['parts'][part]:
                    # need to figure out how to pass id
                    partid = streamdict['parts'][part]['partid']
                    session['partid'] = json.dumps(partid, cls=db.Encoder)[1:-1]
                    return redirect(url_for('parts.overview', part=part))
                else:
                    cursor.vsmap.parts.insert_one({'partname': part})
                    partid = cursor.vsmap.parts.find_one({'partname': part})['_id']
                    streamdict['parts'][part]['partid'] = partid
                    cursor.vsmap.valuestreams.replace_one({'_id':streamdict['_id']}, streamdict)
                    # need to figure out how to pass id
                    session['partid'] = json.dumps(partid, cls=db.Encoder)[1:-1]
                    return redirect(url_for('parts.overview', part=part))

        elif formnum == "2":
            newpart = request.form['newpart']
            if 'parts' in streamdict:
                streamdict['parts'][newpart] = {'name': newpart}
            else:
                streamdict['parts'] = {newpart: {'name': newpart, 'phase': 0}}
            
            if error is not None:
                flash(error)
            else:
                cursor.vsmap.valuestreams.replace_one({'_id':streamdict['_id']}, streamdict)
                return redirect(url_for('streams.overview', stream=stream))
            
        elif formnum == "3":
            from bson.objectid import ObjectId
            cursor.vsmap.valuestreams.delete_one({'_id': ObjectId(streamdict['_id'])})
            return redirect(url_for('index'))

    return render_template('vseditor/overview.html', stream=stream, partlist=partlist, nopartlist=nopartlist)
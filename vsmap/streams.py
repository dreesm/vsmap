from flask import (
    Blueprint, render_template
)

bp = Blueprint('streams', __name__, url_prefix='/valuestreams')

@bp.route('/overview')
def overview():
    return render_template('vseditor/overview.html')
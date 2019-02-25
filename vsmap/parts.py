from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from . import db

bp = Blueprint('parts', __name__, url_prefix='/part')

@bp.route('/<part>/overview', methods=('GET', 'POST'))
def overview(part):
    return render_template('parteditor/overview.html', part=part)
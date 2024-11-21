from flask import Blueprint, render_template

bp = Blueprint('error', __name__, url_prefix='/error')

@bp.route('/')
def error_index():
    return render_template('error.html')

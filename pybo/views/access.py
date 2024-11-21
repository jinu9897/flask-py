from flask import Blueprint, render_template

bp = Blueprint('access', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/graph')
def graph():
    # 그래프 데이터 생성 (예: matplotlib 사용)
    return "Graph Page (그래프를 여기에 추가)"

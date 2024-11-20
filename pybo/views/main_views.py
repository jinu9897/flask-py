from flask import Blueprint, render_template, request
from pybo.calculations import calculate_square, calculate_cube  # 함수 불러오기

bp = Blueprint('main', __name__, url_prefix='/')

# 메인 페이지
@bp.route('/')
def index():
    return render_template('index.html')

# Python 계산 코드 실행
@bp.route('/run_code', methods=['POST'])
def run_code():
    number = int(request.form['number'])  # 사용자 입력 값
    square = calculate_square(number)    # 제곱 계산
    cube = calculate_cube(number)        # 세제곱 계산
    return render_template(
        'index.html',
        number=number,
        square=square,
        cube=cube
    )

import re
import pandas as pd
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, send_file
from io import BytesIO

bp = Blueprint('error', __name__)

@bp.route('/')
def parse_error_log():
    log_file = '/var/log/nginx/error.log'  # 로그 파일 경로

    with open(log_file, 'r') as f:
        text = f.read()

    # 로그 데이터 추출
    pattern = r'([0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}) \[(\w+)\] .*client: ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
    timestamps, log_levels, client_ips = [], [], []
    for match in re.finditer(pattern, text):
        timestamps.append(match.group(1))
        log_levels.append(match.group(2))
        client_ips.append(match.group(3))

    # 데이터프레임 생성
    df = pd.DataFrame({
        "Timestamp": timestamps,
        "Log Level": log_levels,
        "IP": client_ips
    })

    # 시각화: 로그 레벨별 발생 횟수
    most_logs = df['Log Level'].value_counts()
    fig, ax = plt.subplots()
    most_logs.plot(kind='bar', ax=ax, color='lightcoral')
    ax.set_title('Log Levels Frequency')
    ax.set_xlabel('Log Level')
    ax.set_ylabel('Frequency')
    plt.tight_layout()

    # 그래프를 메모리에 저장
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')

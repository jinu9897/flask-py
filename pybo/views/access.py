import re
import pandas as pd
import matplotlib.pyplot as plt
from flask import Blueprint, render_template, send_file
from io import BytesIO

bp = Blueprint('access', __name__)


@bp.route('/')
def parse_access_log():
    log_file = '/var/log/nginx/access.log'  # 로그 파일 경로

    with open(log_file, 'r') as f:
        text = f.read()

    # 로그 데이터 추출
    pattern = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) - - \[(.*?)\] "(.*?)" .* "(.*?)"'
    remote_hosts, times, requests, referrers = [], [], [], []
    for match in re.finditer(pattern, text):
        remote_hosts.append(match.group(1))
        times.append(match.group(2))
        requests.append(match.group(3))
        referrers.append(match.group(4))

    # 데이터프레임 생성
    df = pd.DataFrame({
        "IP": remote_hosts,
        "Time": times,
        "Request": requests,
        "Referrer": referrers
    })

    # 시각화: 상위 10개 IP 요청
    most_ip = df['IP'].value_counts().head(10)
    fig, ax = plt.subplots()
    most_ip.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Top 10 IPs by Request Count')
    ax.set_xlabel('IP Address')
    ax.set_ylabel('Request Count')
    plt.tight_layout()

    # 그래프를 메모리에 저장
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')

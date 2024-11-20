import re
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, send_file
import os

# 로그 파일 경로
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
log_file = os.path.join(BASE_DIR, 'logs', 'access.log')
app = Flask(__name__)

# 그래프 생성 함수
def generate_graph():
    log_file = os.path.join(BASE_DIR, 'logs', 'access.log')
    with open(log_file, 'r') as f:
        text = f.read()

    # 정규 표현식으로 데이터 추출
    remote_hosts = []
    times = []
    requests = []
    referrers = []

    pattern = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) - - \[(.*?)\] "(.*?)" .* "(.*?)"'
    for match in re.finditer(pattern, text):
        remote_hosts.append(match.group(1))  # IP 주소
        times.append(match.group(2))         # 시간
        requests.append(match.group(3))      # 요청
        referrers.append(match.group(4))     # 참조 URL

    data = {"IP": remote_hosts, "Time": times, "Request": requests, "Referrer": referrers}
    df = pd.DataFrame(data)

    # 상위 10개 IP 시각화
    most_ip = df["IP"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 6))
    most_ip.plot(kind='barh', ax=ax, color='skyblue')
    ax.set_title("Top 10 IP Addresses")
    ax.set_xlabel("Count")
    ax.set_ylabel("IP Address")
    ax.invert_yaxis()

    # 그래프를 메모리에 저장
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return img

# 라우트: 메인 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 라우트: 그래프 보기
@app.route('/graph')
def graph():
    img = generate_graph()
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

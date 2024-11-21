from flask import Blueprint, render_template
import re
import pandas as pd
import matplotlib.pyplot as plt
import io
import os
import base64

bp = Blueprint('main', __name__, url_prefix='/')

# 로그 파일 경로
LOG_FILE_PATH = '/var/log/nginx/access.log'

# 메인 페이지
@bp.route('/')
def index():
    # 그래프 데이터를 생성하여 HTML로 전달
    graphs = []
    graphs.append(generate_top_ip_graph())
    graphs.append(generate_top_request_graph())
    graphs.append(generate_top_referrer_graph())
    graphs.append(generate_hourly_request_graph())

    return render_template('index.html', graphs=graphs)


def generate_top_ip_graph():
    """상위 10개 IP 주소 그래프 생성"""
    with open(LOG_FILE_PATH, 'r') as f:
        text = f.read()

    # 데이터 추출
    remote_hosts = []
    pattern = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) - - \[(.*?)\] "(.*?)" .* "(.*?)"'
    for match in re.finditer(pattern, text):
        remote_hosts.append(match.group(1))

    # 데이터프레임 생성
    data = {"IP": remote_hosts}
    df = pd.DataFrame(data)
    most_ip = df["IP"].value_counts().head(10)

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    most_ip.plot(kind='barh', ax=ax, color='skyblue')
    ax.set_title("Top 10 IP Addresses")
    ax.set_xlabel("Request Count")
    ax.set_ylabel("IP Address")
    ax.invert_yaxis()

    # 그래프를 메모리에 저장
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return base64.b64encode(img.getvalue()).decode('utf-8')


def generate_top_request_graph():
    """상위 10개 요청(Request) 그래프 생성"""
    with open(LOG_FILE_PATH, 'r') as f:
        text = f.read()

    # 데이터 추출
    requests = []
    pattern = r'".* (.*?) HTTP/.*"'
    for match in re.finditer(pattern, text):
        requests.append(match.group(1))

    # 데이터프레임 생성
    data = {"Request": requests}
    df = pd.DataFrame(data)
    most_request = df["Request"].value_counts().head(10)

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    most_request.plot(kind='barh', ax=ax, color='lightgreen')
    ax.set_title("Top 10 Requests")
    ax.set_xlabel("Request Count")
    ax.set_ylabel("Request")
    ax.invert_yaxis()

    # 그래프를 메모리에 저장
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return base64.b64encode(img.getvalue()).decode('utf-8')


def generate_top_referrer_graph():
    """상위 10개 참조 URL(Referrer) 그래프 생성"""
    with open(LOG_FILE_PATH, 'r') as f:
        text = f.read()

    # 데이터 추출
    referrers = []
    pattern = r'"- .* "(.*?)"'
    for match in re.finditer(pattern, text):
        referrers.append(match.group(1))

    # 데이터프레임 생성
    data = {"Referrer": referrers}
    df = pd.DataFrame(data)
    most_referrer = df["Referrer"].value_counts().head(10)

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(10, 6))
    most_referrer.plot(kind='barh', ax=ax, color='salmon')
    ax.set_title("Top 10 Referrers")
    ax.set_xlabel("Referrer Count")
    ax.set_ylabel("Referrer")
    ax.invert_yaxis()

    # 그래프를 메모리에 저장
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return base64.b64encode(img.getvalue()).decode('utf-8')


def generate_hourly_request_graph():
    """시간대별 요청(Request) 그래프 생성"""
    with open(LOG_FILE_PATH, 'r') as f:
        text = f.read()

    # 데이터 추출
    times = []
    pattern = r'\[(.*?)\]'
    for match in re.finditer(pattern, text):
        times.append(match.group(1))

    # 시간 데이터를 datetime 형식으로 변환
    data = {"Time": times}
    df = pd.DataFrame(data)
    df["Time"] = pd.to_datetime(df["Time"], format="%d/%b/%Y:%H:%M:%S %z", errors="coerce")

    # 1시간 단위로 그룹화하여 요청 수 집계
    hourly_requests = df.resample('H', on='Time').size()

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(12, 6))
    hourly_requests.plot(kind='line', marker='o', ax=ax, color='skyblue')
    ax.set_title("Requests per Hour")
    ax.set_xlabel("Time")
    ax.set_ylabel("Count")
    ax.grid(True)

    # 그래프를 메모리에 저장
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return base64.b64encode(img.getvalue()).decode('utf-8')

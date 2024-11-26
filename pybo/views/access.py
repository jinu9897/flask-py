'''
import matplotlib
matplotlib.use('Agg')  # 비-GUI 백엔드 설정

import re
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask import Blueprint, render_template

# Blueprint 생성
bp = Blueprint('access', __name__, url_prefix='/')


@bp.route('/')
def access_log():
    # 로그 파일 경로
    log_path = 'pybo/log/access.log'

    # 로그 파일 읽기
    try:
        with open(log_path, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        return "Log file not found."

    # 정규식으로 데이터 추출
    pattern = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) - - \[(.*?)\] "(.*?)" .* "(.*?)"'

    remote_hosts = []
    times = []
    requests = []
    referrers = []

    for match in re.finditer(pattern, text):
        remote_hosts.append(match.group(1))
        times.append(match.group(2))
        requests.append(match.group(3))
        referrers.append(match.group(4))

    # 데이터프레임 생성
    data = {"IP": remote_hosts,
            "Time": times,
            "Request": requests,
            "Referrer": referrers}
    df = pd.DataFrame(data)

    # 데이터 처리
    df["Time"] = pd.to_datetime(df["Time"], format="%d/%b/%Y:%H:%M:%S %z", errors="coerce")
    top_ips = df["IP"].value_counts().head(10)
    top_requests = df["Request"].value_counts().head(10)
    top_referrers = df["Referrer"].value_counts().head(10)
    hourly_requests = df.resample('h', on='Time').size()

    # Referrer 레이블 매핑 생성
    labels = list('abcdefghijklmnopqrstuvwxyz')[:len(top_referrers)]
    referrer_mapping = dict(zip(labels, top_referrers.access))

    # Request 레이블 매핑 생성
    labels = list('abcdefghijklmnopqrstuvwxyz')[:len(top_requests)]
    request_mapping = dict(zip(labels, top_requests.access))

    # 그래프 생성
    ip_graph = generate_graph(top_ips, "Top 10 IP Addresses", "IP", "Count")
    request_graph = generate_graph(top_requests, "Top 10 Requests", "Request", "Count", labels)
    referrer_graph = generate_graph(top_referrers,"Top 10 Referrers","Referrer","Count",labels) # 알파벳 레이블 추가
    hourly_graph = generate_time_graph(hourly_requests, "Requests Per Hour", "Time", "Count")

    # 그래프를 템플릿으로 전달
    return render_template(
        'index.html',
        ip_graph=ip_graph,
        request_graph=request_graph,
        request_mapping=request_mapping,
        referrer_graph=referrer_graph,
        referrer_mapping=referrer_mapping,  # 매핑 전달
        hourly_graph=hourly_graph
    )


def generate_graph(data, title, xlabel, ylabel, labels=None):
    """데이터를 기반으로 그래프 생성 및 Base64 변환"""
    fig, ax = plt.subplots(figsize=(15, 6))

    # y-레이블 변경
    if labels:
        data.access = labels

    data.plot(kind='barh', ax=ax, color='skyblue')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.gca().invert_yaxis()

    # Base64 변환
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_url = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()
    plt.close(fig)
    return f"data:image/png;base64,{graph_url}"


def generate_time_graph(data, title, xlabel, ylabel):
    """시간 데이터를 기반으로 그래프 생성 및 Base64 변환"""
    fig, ax = plt.subplots(figsize=(14, 6))
    data.plot(kind='line', marker='o', ax=ax, color='orange')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()

    # Base64 변환
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_url = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()
    plt.close(fig)
    return f"data:image/png;base64,{graph_url}"
'''

import matplotlib

matplotlib.use('Agg')  # 비-GUI 백엔드 설정

import re
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask import Blueprint, render_template

# Blueprint 생성
bp = Blueprint('access', __name__, url_prefix='/')


@bp.route('/')
def access_log():
    # 로그 파일 경로
    log_path = 'pybo/log/access.log'

    # 로그 파일 읽기
    try:
        with open(log_path, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        return "Log file not found."

    # 정규식으로 데이터 추출
    pattern = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) - - \[(.*?)\] "(.*?)" .* "(.*?)"'

    remote_hosts = []
    times = []
    requests = []
    referrers = []

    for match in re.finditer(pattern, text):
        remote_hosts.append(match.group(1))
        times.append(match.group(2))
        requests.append(match.group(3))
        referrers.append(match.group(4))

    # 데이터프레임 생성
    data = {"IP": remote_hosts,
            "Time": times,
            "Request": requests,
            "Referrer": referrers}
    df = pd.DataFrame(data)

    # 데이터 처리
    df["Time"] = pd.to_datetime(df["Time"], format="%d/%b/%Y:%H:%M:%S %z", errors="coerce")
    top_ips = df["IP"].value_counts().head(10)
    top_requests = df["Request"].value_counts().head(10)
    top_referrers = df["Referrer"].value_counts().head(10)
    hourly_requests = df.resample('h', on='Time').size()

    # Referrer 레이블 매핑 생성
    labels = list('abcdefghijklmnopqrstuvwxyz')[:len(top_referrers)]
    referrer_mapping = dict(zip(labels, top_referrers.index))

    # Request 레이블 매핑 생성
    labels = list('abcdefghijklmnopqrstuvwxyz')[:len(top_requests)]
    request_mapping = dict(zip(labels, top_requests.index))

    # 그래프 생성
    ip_graph = generate_graph(top_ips, "Top 10 IP Addresses", "IP", "Count")
    request_graph = generate_graph(top_requests, "Top 10 Requests", "Request", "Count", labels)
    referrer_graph = generate_graph(top_referrers,"Top 10 Referrers","Referrer","Count",labels) # 알파벳 레이블 추가
    hourly_graph = generate_time_graph(hourly_requests, "Requests Per Hour", "Time", "Count")

    # 그래프를 템플릿으로 전달
    return render_template(
        'index.html',
        ip_graph=ip_graph,
        request_graph=request_graph,
        request_mapping=request_mapping,
        referrer_graph=referrer_graph,
        referrer_mapping=referrer_mapping,  # 매핑 전달
        hourly_graph=hourly_graph
    )



def generate_graph(data, title, xlabel, ylabel, labels=None):
    """데이터를 기반으로 그래프 생성 및 Base64 변환"""
    fig, ax = plt.subplots(figsize=(14, 6))

    # y-레이블 변경
    if labels:
        data.index = labels

    data.plot(kind='barh', ax=ax, color='skyblue')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.gca().invert_yaxis()

    # Base64 변환
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_url = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()
    plt.close(fig)
    return f"data:image/png;base64,{graph_url}"


def generate_time_graph(data, title, xlabel, ylabel):
    """시간 데이터를 기반으로 그래프 생성 및 Base64 변환"""
    fig, ax = plt.subplots(figsize=(13, 6))
    data.plot(kind='line', marker='o', ax=ax, color='orange')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()

    # Base64 변환
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_url = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()
    plt.close(fig)
    return f"data:image/png;base64,{graph_url}"

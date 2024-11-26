import matplotlib
matplotlib.use('Agg')  # 비-GUI 백엔드 설정

import re
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask import Blueprint, render_template

# Blueprint 생성
bp = Blueprint('error', __name__, url_prefix='/error')

@bp.route('/')
def error_log():
    # 로그 파일 경로
    log_path = 'pybo/log/error.log'

    # 로그 파일 읽기
    try:
        with open(log_path, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        return "Log file not found."

    # 정규식으로 데이터 추출
    pattern = r'([0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}) \[(\w+)\] .*client: ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'

    timestamps = []
    log_levels = []
    client_ips = []

    for match in re.finditer(pattern, text):
        timestamps.append(match.group(1))
        log_levels.append(match.group(2))
        client_ips.append(match.group(3))

    # 데이터프레임 생성
    data = {"Timestamp": timestamps,
            "Log Level": log_levels,
            "IP": client_ips}
    df = pd.DataFrame(data)

    # 데이터 처리
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    top_ips = df["IP"].value_counts().head(10)
    top_logs = df["Log Level"].value_counts().head(10)
    hourly_errors = df.resample('h', on='Timestamp').size()

    # 그래프 생성
    ip_graph = generate_graph(top_ips, "Top 10 IP Addresses", "IP", "Count")
    log_graph = generate_graph(top_logs, "Top 10 Log Levels", "Log Level", "Count")
    hourly_graph = generate_time_graph(hourly_errors, "Errors Per Hour", "Time", "Count")

    # 그래프를 템플릿으로 전달
    return render_template(
        'error.html',
        ip_graph=ip_graph,
        log_graph=log_graph,
        hourly_graph=hourly_graph
    )

def generate_graph(data, title, xlabel, ylabel):
    """데이터를 기반으로 그래프 생성 및 Base64 변환"""
    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot(kind='barh', ax=ax, color='salmon')
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
    fig, ax = plt.subplots(figsize=(12, 6))
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
@bp.route('/')
def error_log():
    # 더미 데이터 예시
    data = {'Log': ['ERROR', 'WARN'], 'Count': [7, 5]}
    df = pd.DataFrame(data)
    graph = generate_graph(df)
    return render_template('error.html', graph=graph)

def generate_graph(df):
    """데이터프레임을 기반으로 그래프 생성"""
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(kind='barh', ax=ax, color='salmon')
    ax.set_title('Top 10 Error Logs')
    ax.set_xlabel('Count')
    ax.set_ylabel('Log Type')

    # 그래프를 Base64로 변환
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_url = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()
    plt.close(fig)
    return f"data:image/png;base64,{graph_url}"
'''

'''
@bp.route('/')
def error_log():
    # 에러 로그 분석 결과 반환
    return "Error log analysis page"


def error_analysis():
    with open('log/error.log', 'r') as f:
        text = f.read()

    # 정규식으로 데이터 추출
    pattern = r'([0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}) \[(\w+)\] .*client: ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
    timestamps, log_levels, client_ips = [], [], []
    for match in re.finditer(pattern, text):
        timestamps.append(match.group(1))
        log_levels.append(match.group(2))
        client_ips.append(match.group(3))

    df = pd.DataFrame({"Timestamp": timestamps, "Log Level": log_levels, "IP": client_ips})
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')

    # 데이터 집계
    top_ips = df["IP"].value_counts().head(10)
    top_logs = df["Log Level"].value_counts().head(10)
    hourly_errors = df.resample('H', on='Timestamp').size()

    # 그래프 생성
    graphs = []
    fig, ax = plt.subplots(figsize=(10, 6))
    top_ips.plot(kind='barh', ax=ax, color='pink')
    ax.set_title('Top 10 IPs in Error Logs')
    ax.set_xlabel('Count')
    ax.set_ylabel('IP Address')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graphs.append(base64.b64encode(buf.getvalue()).decode('utf8'))
    plt.close()

    fig, ax = plt.subplots(figsize=(10, 6))
    top_logs.plot(kind='barh', ax=ax, color='purple')
    ax.set_title('Top 10 Log Levels')
    ax.set_xlabel('Count')
    ax.set_ylabel('Log Level')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graphs.append(base64.b64encode(buf.getvalue()).decode('utf8'))
    plt.close()

    return graphs
'''
from flask import Blueprint, render_template
import re
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

bp = Blueprint('error', __name__, url_prefix='/error')

@bp.route('/')
def error_index():
    log_file_path = '/var/log/nginx/error.log'  # 로그 파일 경로

    # 로그 파일 읽기
    with open(log_file_path, 'r') as f:
        text = f.read()

    # 데이터 추출
    timestamps = []
    log_levels = []
    client_ips = []

    pattern = r'([0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}) \[(\w+)\] .* ".*\n.*\n.*" .*, client: ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
    for match in re.finditer(pattern, text):
        timestamps.append(match.group(1))
        log_levels.append(match.group(2))
        client_ips.append(match.group(3))

    data = {"Timestamp": timestamps, "Log Level": log_levels, "IP": client_ips}
    df = pd.DataFrame(data)

    # 가장 많이 발생한 IP 주소 시각화
    most_ip = df["IP"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    most_ip.plot(kind='barh', ax=ax, color='skyblue')
    ax.set_title('Top 10 IP Addresses by Request Count')
    ax.set_xlabel('Request Count')
    ax.set_ylabel('IP Address')
    ax.invert_yaxis()
    ip_img = io.BytesIO()
    plt.savefig(ip_img, format='png', bbox_inches='tight')
    ip_img.seek(0)
    plt.close(fig)

    # 가장 많이 발생한 로그레벨 시각화
    most_log = df['Log Level'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    most_log.plot(kind='barh', ax=ax, color='lightgreen')
    ax.set_title('Top 10 Log Level')
    ax.set_xlabel('Count')
    ax.set_ylabel('Log Level')
    ax.invert_yaxis()
    log_img = io.BytesIO()
    plt.savefig(log_img, format='png', bbox_inches='tight')
    log_img.seek(0)
    plt.close(fig)

    # 시간대별 타임스탬프 시각화
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    hourly_Timestamp = df.resample('h', on='Timestamp').size()
    fig, ax = plt.subplots(figsize=(12, 6))
    hourly_Timestamp.plot(kind='line', marker='o', ax=ax, color='skyblue')
    ax.set_title('Timestamp per Hour')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Count')
    ax.grid(True)
    time_img = io.BytesIO()
    plt.savefig(time_img, format='png', bbox_inches='tight')
    time_img.seek(0)
    plt.close(fig)

    # 그래프 이미지를 base64로 변환
    images = {
        "ip": base64.b64encode(ip_img.getvalue()).decode('utf-8'),
        "log": base64.b64encode(log_img.getvalue()).decode('utf-8'),
        "time": base64.b64encode(time_img.getvalue()).decode('utf-8')
    }

    return render_template('error_index.html', images=images)

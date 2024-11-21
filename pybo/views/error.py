import re
import pandas as pd
import matplotlib.pyplot as plt

# 로그 파일 읽기 및 데이터 추출
with open('/content/error.log', 'r') as f:
    text = f.read()

# 추출할 데이터를 저장할 배열
timestamps = []
log_levels = []
client_ips = []

# 정규 표현식 패턴 정의 및 데이터 추출
pattern = r'([0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}) \[(\w+)\] .* ".*\n.*\n.*" .*, client: ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
for match in re.finditer(pattern, text):
    timestamps.append(match.group(1))  # 타임스탬프
    log_levels.append(match.group(2))  # 로그 레벨 (error, warn 등)
    client_ips.append(match.group(3))  # 클라이언트 IP

data = {"Timestamp": timestamps,
        "Log Level": log_levels,
        "IP": client_ips}

df = pd.DataFrame(data)

# 가장 많이 발생한 IP 주소 추출
Most_IP = df["IP"].value_counts().reset_index()
Most_IP.columns = ["IP", "Count"]
Plt_Most_IP = Most_IP.head(10)

# 가장 많이 발생한 로그레벨 추출
Most_Log = df['Log Level'].value_counts().reset_index()
Most_Log.columns = ["Log", "Count"]
Plt_Most_Log = Most_Log.head(10)

# Timestamp 열을 datetime 형식으로 변환 (에러 발생 시 NaT로 처리)
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

# 1시간 단위로 그룹화하여 요청 수 집계
hourly_Timestamp = df.resample('h', on='Timestamp').size()

# 상위 10개 IP 주소 시각화
plt.figure(figsize=(10, 6))
plt.barh(Plt_Most_IP['IP'], Plt_Most_IP['Count'], color='skyblue')
plt.xlabel('Request Count')
plt.ylabel('IP Address')
plt.title('Top 10 IP Addresses by Request Count')
plt.gca().invert_yaxis()  # 상위 항목이 위에 오도록 반전
plt.show()

# 상위 10개 로그레벨 시각화
plt.figure(figsize=(10, 6))
plt.barh(Plt_Most_Log['Log'], Plt_Most_Log['Count'], color='lightgreen')
plt.xlabel('Count')
plt.ylabel('Log Level')
plt.title('Top 10 Log Level')
plt.gca().invert_yaxis()
plt.show()

# 시간대별 타임스탬프 시각화
plt.figure(figsize=(12, 6))
hourly_Timestamp.plot(kind='line', marker='o', color='skyblue')
plt.xlabel('Timestamp')
plt.ylabel('Count')
plt.title('Timestamp per Hour')
plt.grid(True)
plt.tight_layout()
plt.show()
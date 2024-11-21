import re
import pandas as pd
import matplotlib.pyplot as plt

# 로그 파일 읽기 및 데이터 추출
with open('/content/access.log', 'r') as f:
    text = f.read()

# 추출할 데이터를 저장할 배열
remote_hosts = []
times = []
requests = []
referrers = []

# 정규 표현식 패턴 정의 및 데이터 추출
pattern = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) - - \[(.*?)\] "(.*?)" .* "(.*?)"'
for match in re.finditer(pattern, text):
    remote_hosts.append(match.group(1))  # IP 주소
    times.append(match.group(2))         # 시간
    requests.append(match.group(3))      # 요청
    referrers.append(match.group(4))     # 참조 URL

data = {"IP": remote_hosts,
        "Time": times,
        "Request": requests,
        "Referrer": referrers}

df = pd.DataFrame(data)

# 가장 많이 발생한 IP 주소 추출
Most_IP = df["IP"].value_counts().reset_index()
Most_IP.columns = ["IP", "Count"]
Plt_Most_IP = Most_IP.head(10)

# 가장 많이 발생한 요청 추출
Most_Request = df['Request'].value_counts().reset_index()
Most_Request.columns = ["Request", "Count"]
Plt_Most_Request = Most_Request.head(10)

# 가장 많이 발생한 참조 URL 추출
Most_Referrer = df['Referrer'].value_counts().reset_index()
Most_Referrer.columns = ["Referrer", "Count"]
Plt_Most_Referrer = Most_Referrer.head(10)

# Time 열을 datetime 형식으로 변환 (에러 발생 시 NaT로 처리)
df["Time"] = pd.to_datetime(df["Time"], format="%d/%b/%Y:%H:%M:%S %z", errors="coerce")

# 1시간 단위로 그룹화하여 요청 수 집계
hourly_requests = df.resample('H', on='Time').size()

# 상위 10개 IP 주소 시각화
plt.figure(figsize=(10, 6))
plt.barh(Plt_Most_IP['IP'], Plt_Most_IP['Count'], color='skyblue')
plt.xlabel('Request Count')
plt.ylabel('IP Address')
plt.title('Top 10 IP Addresses by Request Count')
plt.gca().invert_yaxis()  # 상위 항목이 위에 오도록 반전
plt.show()

# 상위 10개 요청(Request) 시각화
plt.figure(figsize=(10, 6))
plt.barh(Plt_Most_Request['Request'], Plt_Most_Request['Count'], color='lightgreen')
plt.xlabel('Request Count')
plt.ylabel('Request')
plt.title('Top 10 Requests')
plt.gca().invert_yaxis()
plt.show()

# 상위 10개 참조 URL(Referrer) 시각화
plt.figure(figsize=(10, 6))
plt.barh(Plt_Most_Referrer['Referrer'], Plt_Most_Referrer['Count'], color='salmon')
plt.xlabel('Referrer Count')
plt.ylabel('Referrer')
plt.title('Top 10 Referrers')
plt.gca().invert_yaxis()
plt.show()

# 시간대별 요청 수 시각화
plt.figure(figsize=(12, 6))
hourly_requests.plot(kind='line', marker='o', color='skyblue')
plt.xlabel('Time')
plt.ylabel('Count')
plt.title('Requests per Hour')
plt.grid(True)
plt.tight_layout()
plt.show()
import urllib.request  # urllib.request : 웹상의 URL 주소에 접속하여 데이터를 가져오는 라이브러리
import json            # 서버에서 보낸 JSON 데이터를 파이썬 딕셔너리 형태로 변환해주는 라이브러리

# OpenWeatherMap 사이트에서 발급받은 고유 인증 
api_key = '48fde1e95a9d04732d98226e3be018a7'

# q=Seoul(도시), units=metric(섭씨온도), lang=en(영어), cnt=8(3시간 단위로 8개 예보 가져오기)
url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"

# r.read()로 가져온 raw 데이터를 json.loads를 통해 파이썬이 이해할 수 있는 구조로 변환
with urllib.request.urlopen(url) as r:
    data = json.loads(r.read())

# 시간(time) 추출 : 'dt_txt' 문자열에서 시간(11~13자)만 잘라 숫자로 바꾼 후, 
# 한국 표준시(UTC+9)를 적용하고 24시간제로 계산 (% 24)
time = [(int(item['dt_txt'][11:13]) + 9) % 24 for item in data['list']]

# 기온(temp) 추출 : 'main' 항목 안에 들어있는 'temp' 값을 리스트에 담음
temp = [item['main']['temp'] for item in data['list']]

# 습도(humi) 추출 : 'main' 항목 안에 들어있는 'humidity' 값을 리스트에 담음
humi = [item['main']['humidity'] for item in data['list']]

# 날씨 설명(desc) 추출 : 'weather' 리스트의 첫 번째 항목에 담긴 날씨 묘사 문구를 가져옴
desc = [item['weather'][0]['description'] for item in data['list']]

print(time)    # 예보 시간대 리스트
print(temp)    # 기온 데이터 리스트
print(humi)    # 습도 데이터 리스트
print(desc)    # 날씨 상태 리스

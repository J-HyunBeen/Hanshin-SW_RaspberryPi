import urllib.request    # urllib.request : 특정 URL 주소에 접속하여 데이터를 요청하기 위한 라이브러
import json              # JSON : 서버로부터 받은 JSON 형식의 데이터를 파이썬 딕셔너리로 변환해주는 라이브러리


# OpenWeatherMap 사이트에서 발급받은 고유 인증 키
api_key = '48fde1e95a9d04732d98226e3be018a7'

# API 주소 구성 : 도시(Seoul), 인증키, 단위(metric : 섭씨온도), 언어 등을 조합한 URL 생성
url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"



with urllib.request.urlopen(url) as r:                               # 설정한 URL 주소로 접속 시도
    data = json.loads(r.read())                                      # 읽어온 원시 데이터를 파이썬이 이해하는 딕셔너리 형태로 변환하여 저장

text = ""                                                            # 추출한 날씨 정보들을 하나로 합쳐서 담아둘 빈 변수 생성
for i in range(8):                                                   # 가져온 8개의 예보 데이터(24시간분)를 하나씩 꺼내어 반복 처리
    item = data['list'][i]
    
    hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)       # dt_txt에서 시간 부분만 잘라 숫자로 바꾼 뒤 9를 더함. zfill(2)는 '03시'처럼 두 자리 형식을 맞추는 기능
    
    temp = item['main']['temp']                # 현재 온도 추출
    humi = item['main']['humidity']            # 현재 습도 추출
    desc = item['weather'][0]['description']   # 날씨 상태 설명 추출

    # 추출한 정보들을 괄호() 안에 담아 하나의 문장으로 이어 붙임
    # 예: (18h 15.2C 27% clear sky)
    text = text + "(" + str(hour) + "h "
    text = text + str(temp) + "C "
    text = text + str(humi) + "% "
    text = text + str(desc) + ")"
    
# 8개의 예보가 모두 합쳐진 긴 문자열을 터미널에 한 줄로 출력
print(text)

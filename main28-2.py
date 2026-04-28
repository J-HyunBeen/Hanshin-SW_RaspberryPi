import urllib.request        # 웹상의 데이터 요청 라이브러리
import json                  # 데이터를 파이썬 딕셔너리로 변환하는 라이브러리
import datetime              # 현재 날짜와 시간 정보를 얻기 위한 라이브러리
import asyncio               # 여러 작업을 동시에 처리하기 위한 비동기 제어 모
from telegram import Bot     # 텔레그램 봇을 제어하기 위한 전용 클래스

telegram_id = '8210798076'                                      # 메시지를 받을 사용자의 고유 ID
my_token = '8788783011:AAFWfn213e4UEn3E954XM9kBxa3MK8yjHC4'     # 텔레그램 봇 인증 토큰
api_key = '48fde1e95a9d04732d98226e3be018a7'                    # OpenWeatherMap 인증 키


# 텔레그램 봇 객체 생성 및 초기화
bot = Bot(token=my_token)


# 알림 예약 시간 설정 (시간 단위 및 특정 분 단위)
ALERT_HOURS = [7, 10, 13, 16, 19, 22]           # 정시 알림 : 3시간 간격 설정                            
ALERT_TIMES = ["18:22", "20:20"]                # 사용자 지정 알림 : 특정 시각 설정                       

def getWeather():
    # API 주소 구성 : 서울 날씨, 섭씨 온도, 8개 예보 데이터 요청
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"

    with urllib.request.urlopen(url) as r:
        # 수신 데이터를 파이썬 딕셔너리 형태로 변환
        data = json.loads(r.read())

    text = ""
    for i in range(8):                                                # 3시간 간격의 예보 8개를 반복하며 문자열 생성
        item = data['list'][i]
        hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)    # 시간 추출 및 한국 시간(+9) 보정 후 두 자리 형식으로 맞춤
        temp = item['main']['temp']                                   # 기온 추출
        humi = item['main']['humidity']                               # 습도 추출
        desc = item['weather'][0]['description']                      # 날씨 상태 추출
        text += f"({hour}h {temp}C {humi}% {desc})\n"                 # 텔레그램 메시지용 문자열 조합

    return text

async def main():
    try:
        while True:                            # 무한 루프를 돌며 실시간 시간 감시
            now = datetime.datetime.now()      # 현재 시간 가져오기
            hm = now.strftime('%H:%M')         # '시:분' 형식으로 변환                           


            # 알림 조건 확인 : 정시 알람 혹은 특정 예약 시각인지 체크
            is_alert_hour = now.hour in ALERT_HOURS and now.minute == 0 and now.second == 0   
            is_alert_time = hm in ALERT_TIMES and now.second == 0                         

            if is_alert_hour or is_alert_time:
                msg = getWeather()    # 날씨 정보 생성
                print(msg)            # 확인용 터미널 출력
                # 텔레그램으로 날씨 정보 전송 (비동기 방식)
                await bot.send_message(chat_id=telegram_id, text=msg)
                
            # CPU 과부하 방지 및 1초 간격 체크를 위해 대기
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        pass

asyncio.run(main())

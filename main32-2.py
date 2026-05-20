import speech_recognition as sr  # 음성 인식(STT) 처리를 위한 라이브러리
import requests                  # OpenWeatherMap API에 기상 데이터를 요청하기 위한 라이브러리
import os                        # espeak 리눅스 터미널 명령어를 실행하기 위한 라이브러리
import time                      # 시간 지연 등의 처리를 위한 라이브러리 (현재 코드에서는 대기용)

# OpenWeatherMap에서 발급받은 개인 API 인증 키 및 서울 지역 날씨 요청 URL 설정
API_KEY = "48fde1e95a9d04732d98226e3be018a7"
url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"

# espeak 엔진을 사용해 문자열을 음성(TTS)으로 출력하는 사용자 정의 함수
def speak(option, msg):
    # os.system을 통해 리눅스 환경의 espeak 명령어를 호출하여 음성을 재생함
    os.system("espeak {} '{}'".format(option, msg))

try:
    # 프로그램이 강제 종료(Ctrl+C)되기 전까지 무한 반복 구동
    while True:
        r = sr.Recognizer()  # 음성 인식을 수행하는 Recognizer 객체 생성
        
        # 시스템의 기본 마이크를 오디오 소스로 지정하여 사용
        with sr.Microphone() as source:
            print("Say something!")  # 사용자에게 말하라는 안내 메시지 출력
            audio = r.listen(source) # 마이크로부터 음성 신호를 입력받아 오디오 데이터로 저장
            
        try:
            # 구글 웹 스피치 API를 활용하여 오디오를 한국어 텍스트로 변환 (STT 변환)
            text = r.recognize_google(audio, language='ko-KR')
            print("You said: " + text) # 인식된 텍스트 화면에 표시
            
            # 인식된 말 속에 '날씨'라는 핵심 키워드가 포함되어 있는지 조건 검사
            if text in "날씨":
                print("날씨 음성을 인식하였습니다.")
                
                # requests 라이브러리로 날씨 API에 접속하여 기상 데이터(JSON 형식) 받아오기
                response = requests.get(url)
                data = response.json()      # 가독성을 위해 파이썬 딕셔너리 구조로 변환
                
                temp = data["main"]["temp"]       # 딕셔너리에서 현재 기온 추출
                humi = data["main"]["humidity"]   # 딕셔너리에서 현재 습도 추출
                
                # 안내 멘트 생성 (소수점 자리를 없애기 위해 기온은 정수형(int)으로 변환 후 결합)
                msg = '    기온은 ' + str(int(temp)) + '도 습도는 ' + str(humi) + '퍼센트 입니다'
                
                # espeak 전용 옵션 설정 (-s: 속도 180, -p: 음높이 50, -a: 볼륨 200, -v: 한국어 여성 voice)
                option = '-s 180 -p 50 -a 200 -v ko+f5'
                speak(option, msg) # 설정한 옵션과 메시지를 바탕으로 TTS 함수 실행
            
        # 음성 인식이 흐리거나 주변 소음 등으로 텍스트 변환에 실패했을 때의 예외 처리
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        # 네트워크 단절이나 API 서버 오류 등으로 구글 서비스 요청이 불가능할 때의 예외 처리
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

# 사용자가 키보드로 Ctrl+C를 눌러 프로그램을 수동 종료했을 때 발생하는 예외를 안전하게 처리
except KeyboardInterrupt:
    pass

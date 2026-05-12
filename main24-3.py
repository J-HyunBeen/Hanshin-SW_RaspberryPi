import urllib.request, json, tkinter, tkinter.font   
# urlib.request : 특정 URL 주소에 접속하여 데이터를 요청하기 위한 모듈
# json : 서버로부터 받은 JSON 형식의 데이터를 파이썬 딕셔너리로 변환하기
# tkinter : 파이썬 기본 윈도우 창을 만들기 위한 모듈
# tkinter.font : 윈도우 창 내부 글꼴을 세밀하게 설정하기 위한 모듈



API_KEY = "48fde1e95a9d04732d98226e3be018a7"
# OpenWeatherMap 사이트에서 발급받은 고유 인증 키

# 핵심 로직 함수 : 1분마다 날씨 정보를 갱신하는 함
def tick1Min():
    # API 주소 구성 : 도시(Seoul), 인증키, 단위(metric : 섭씨온도)를 조합한 URL 생성
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"
 
    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())             # r.read()로 읽어온 원시 데이터를 json.loads를 통해 파이썬이 이해하는 딕셔너리 형태로 변
        print(data)                             # 데이터 구조 파악을 위해 터미널에 전체 데이터 출력

 
    temp = data["main"]["temp"]       # 현재 온도 추출
    humi = data["main"]["humidity"]   # 현재 습도 추출
 
    label.config(text=f"{temp:.1f}C   {humi}%")  # Tkinter 라벨(label)의 텍스트를 실시간 데이터로 변경
                                                 # .1f는 소수점 첫째 자리까지만 표시하라는 의미
    # 60,000밀리초 (60초) 후에 다시 이 함수를 실행하도록 예약
    # GUI 환경에서는 time.sleep을 쓰면 창이 멈추기 때문에 반드시 after()를 써야 함
    window.after(60000, tick1Min) 
 
window = tkinter.Tk()                                    # 메인 윈도우 창 생성
window.title("TEMP HUMI DISPLAY")                        # 창 제목 설정
window.geometry("400x100")                               # 창 크기 설정 (가로 400, 세로 100)
window.resizable(False, False)                           # 창 크기를 사용자가 임의로 조절하지 못하게 고
font = tkinter.font.Font(size=30)                        # 글꼴 설정 : 크기를 30으로 지정하여 가독성을 높임
label = tkinter.Label(window, text="", font=font)        # 라벨 위젯 생성 : 텍스트가 표시될 공간을 만들고 폰트 적용
label.pack()                                             # 라벨을 화면 중앙에 배치

tick1Min()                                               # 프로그램 시작 시 최초 1회 날씨 정보 가져오기 시작
window.mainloop()                                        # 윈도우 창이 닫히지 않고 계속 유지되도록 메인 루프 실행

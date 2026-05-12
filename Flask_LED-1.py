from flask import Flask, request, render_template		# 1. 라이브러리 로드 : 프로젝트에 필요한 도구를 가져오는 단계
														# Flask : 웹 서버 기능을 제공하는 프레임워크
														# request : 브라우저가 보내온 데이터를 읽기 위한 도구
														# render_template : 준비된 HTML 파일을 화면에 띄워주는 도구
from gpiozero import LED								# 출력 장치인 LED를 제어하기 위한 전용 클래스를 불러옴

app = Flask(__name__)									# 2. 객체 생성 및 초기화 : 하드웨어와 소프트웨어를 매핑하는 단계

red_led = LED(21)										# 라즈베리 GPIO 21번핀에 LED 연결 

@app.route('/')											# 3. 라우팅 : 특정 주소로 접속했을 때 실행할 동작 정의
def home():		# 사용자가 브라우저 주소창에 IP를 입력하고 처음 들어왔을 때 실행.
				# templates 폴더 내의 index.html 파일을 읽어 화면을 사용자에게 보여줌.											
	return render_template("index.html")				
	
@app.route('/data', methods = ['POST'])
def data():
			# 웹 페이지의 버튼 클릭으로 전송된 데이터를 처리하는 핵심 로직
	
	data = request.form['led']		# 사용자가 웹에서 보낸 폼 데이터 중 'led'라는 이름을 가진 값을 변수에 저장
									# ex) on 버튼을 누르면 data 변수에 on이 담김
	if(data == 'on'):
		red_led.on()				# GPIO 21번 핀에 전압 인가 (LED 점등)
		
	elif(data == 'off'):
		red_led.off()				# GPIO 21번 핀에 전압 차단 (LED 소등)
		
	return home()					# 데이터 처리 후 다시 초기 화면을 호출하여 상태 유지 및 화면 갱신


if __name__ == "__main__":

	# host = "0.0.0.0": 같은 와이파이를 쓰는 스마트폰이나 PC에서도 접속이 가능하도록 개방
	# port = "80": 웹 접속의 표준 포트(80)를 사용하여 주소 입력 편의성 제공	
	app.run(host = "0.0.0.0", port = "80")

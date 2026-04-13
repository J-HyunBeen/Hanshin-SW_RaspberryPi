from flask import Flask, request, render_template	# 웹 서버 구축 및 데이터 처리를 위한 Flask, request, render_template 라이브러리
from gpiozero import LED							# 라즈베리 파이 GPIO 제어를 위한 라이브러

app = Flask(__name__)								# Flask 객체 생성 : 현재 파일(__name__)을 기준으로 웹 애플리케이션 초기화

red_led = LED(21)									# 제어할 LED 객체 설정 : GPIO 21번 핀에 연결된 LED 선언

@app.route('/')										# 메인 페이지 접속 시 실행되는 함수 ('/')
def home():
	return render_template("index.html")			# templates 폴더 안에 있는 index.html 파일을 랜더링하여 사용자에게 보여줌
	
@app.route('/data', methods = ['POST'])				# 데이터 전송시 실행되는 함수 ('/data')
def data():											# HTML 폼(Form)에서 POST 방식으로 데이터를 보낼 때 동작함
	data = request.form['led']						# HTML의 input 태그 중 name이 'led'인 요소의 값을 가져옴 (on 또는 off)
	
	if(data == 'on'):								# 가져온 데이터가 'on'일 경우 LED 점등
		red_led.on()
		
	elif(data == 'off'):							# 가져온 데이터가 'off'일 경우 LED 소등
		red_led.off()
		
	return home()									
	
if __name__ == "__main__":							# host = "0.0.0.0" : 같은 네트워크 내의 모든 기기에서 접속 허용
	app.run(host = "0.0.0.0", port = "80")			# port = "80": HTTP 기본 포트인 80번 포트 사용

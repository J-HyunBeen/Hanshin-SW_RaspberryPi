from gpiozero import MotionSensor		# PIR 센서를 제어하기 위한 모듈
import time								# 시간 지연(sleep)을 위한 모듈
from picamera2 import Picamera2			# 라즈베리 파이 카메라 제어 모듈
import datetime							# 파일명에 사용할 현재 시간 정보를 얻기 위한 모듈

pirPin = MotionSensor(16)				# GPIO 16번 핀에 연결된 PIR 센서를 'pirPin'이라는 객체로 정의

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()	# 카메라 미리보기 설정 생성
picam2.configure(camera_config)							# 설정 적용
picam2.start()											# 카메라 모듈 가동

try:
	while True:											# 무한 루프를 돌며 움직임 감시
		try:
			sensorValue = pirPin.value							# 센서 값을 읽어옴 (움직임 감지 시 1, 평상시 0)
			if sensorValue ==1:									# 조건문 : 움직임이 감지(1) 되었을 때 실행
				now = datetime.datetime.now()					# 현재 날짜와 시간 정보 가져오기
				print(now)										# 터미널에 감지 시간 출력
				fileName = now.strftime('%y-%m-%d %H:%M:%s')	# 파일명 생성 : '년-월-일 시:분:초' 형식으로 문자열 변환	
				picam2.capture_file(fileName + '.jpg')			# 사진 촬영 및 저장 : 파일명.jpg 형식으로 저장
				time.sleep(0.5)									# 연속 촬영 방지 및 센서 안정화를 위해 0.5초 대기
				
		except:
			pass		# 루프 도중 발생할 수 있는 사소한 오류무시

except KeyboardInterrupt:	# 사용자가 Ctrl+C를 눌러 프로그램을 종료했을 때의 안전 장치
	pass

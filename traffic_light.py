from gpiozero import LED				# 라즈베리 파이 GPIO 제어를 위한 LED 클래스 불러오기
from time import sleep					# 일정 시간 동안 동작을 지연시기키 위한 함수(sleep) 불러오기



# --- 핀 번호 설정 ---
# 각 변수에 연결된 라즈베리 파이의 GPIO 핀 번호를 할당합니다.
carLedRed	= 2							# 차량용 빨간색 LED (GPIO 2번 핀)
carLedYellow	= 3						# 차량용 노란색(파란색) LED (GPIO 3번 핀)
carLedGreen	= 4							# 차량용 초록색 LED (GPIO 4번 핀)
humanLedRed	= 20						# 보행자용 빨간색 LED (GPIO 20번 핀)
humanLedGreen = 21						# 보행자용 초록색 LED (GPIO 21번 핀)

carLedRed		= LED(2)
carLedYellow	= LED(3)
carLedGreen		= LED(4)
humanLedRed		= LED(20)
humanLedGreen	= LED(21)

try:									# 프로그램이 종료될 때까지 무한 반복
	while 1:							# [신호 1] 차량 : 초록불 / 보행자 : 빨간불 (차량 주행 중)
		carLedRed.value = 0				# 0은 전압을 차단하여 LED에 불이 들어오지 않음
		carLedYellow.value = 0			
		carLedGreen.value = 1			# 1은 전압을 인가하여 LED에 불이 들어옴
		humanLedRed.value = 1			
		humanLedGreen.value = 0
		sleep(3.0)						# 이 상태를 3초간 유지

										# [신호 2] 차량 : 노란불(파란불) / 보행자 : 빨간불 (신호 변경 구간)
		carLedRed.value = 0
		carLedYellow.value = 1			# 차량 정지를 위해 노란불(파란불) 점등
		carLedGreen.value = 0
		humanLedRed.value = 1			# 보행자는 여전히 대기
		humanLedGreen.value = 0
		sleep(1.0)						# 이 상태를 1초간 유지

										# [신호 3] 차량 : 빨간불 / 보행자 : 초록불 (보행자 횡단)
		carLedRed.value = 1				# 차량 정지
		carLedYellow.value = 0
		carLedGreen.value = 0
		humanLedRed.value = 0
		humanLedGreen.value = 1			# 보행자 횡단
		sleep(3.0)						# 이 상태를 3초간 유지
		
except KeyboardInterrupt:				# Ctrl+C를 입력 -> except 문으로 안전하게 이동
    pass

		
		
carLedRed.value = 0						# 모든 LED의 전압을 차단하여 불을 끕니다
carLedYellow.value = 0
carLedGreen.value = 0
humanLedRed.value = 0
humanLedGreen.value = 0
		

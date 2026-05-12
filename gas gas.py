from gpiozero import DigitalInputDevice    # DigitalInputDevice : 센서로부터 0 또는 1의 디지털 신호를 읽어오기 위해 사용
from gpiozero import OutputDevice          # OutputDevice : 부저나 LED 같은 출력 장치에 전기를 보내거나 끊기 위해 사용
import time

bz = OutputDevice(18)                      # GPIO 18번 핀에 연결된 부저를 'bz'라는 객체로 설정
gas = DigitalInputDevice(17)               # GPIO 17번 핀에 연결된 가스 센서를 'gas'라는 객체로 설정

try:
    while True:                            # 무한 반복하며 가스 상태 감시
        if gas.value == 0:                 # 가스 센서의 값을 확인 ( 가스 감지 시 0, 평상시 1인 경우 )
            print("gas gas")               # 만약 센서 값이 0이라면 (가스가 감지되었다면)
            bz.on()                        # 터미널에 경고 문구 출력 및 GPIO 18번 핀에 전압을 인가하여 부저가 울림
        else:                    # 가스가 감지되지 않는다면 (평상시)
            print("Ture")        # 터미널에 정상 상태 출력
            bz.off()             # GPIO 18번 핀의 전압을 차단하여 부저를 끔
            
        time.sleep(0.2)          # CPU 과부하를 방지하고 센서의 측정 간격을 위해 0.2초 대기
        
except KeyboardInterrupt:        # 사용자가 Ctrl+C를 눌러 프로그램을 멈췄을 때 실행
    pass

bz.off()         # 프로그램이 종료될 때 부저가 켜져 있다면 안전하게 끄기




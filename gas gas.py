from gpiozero import DigitalInputDevice        # 디지털 입력 장치(감지센서) 제어를 위한 클래스 불러오기
from gpiozero import OutputDevice              # 출력 장치(부저) 제어를 위한 클래스 불러오기
import time                                    # 시간 지연(sleep)을 위한 모듈 불러오


#----- 하드웨어 설정-------
# GPIO 18번 핀에 연결된 bz(부저) 객체 생성
bz = OutputDevice(18)
# GPIO 17번 핀에 연결된 가스 감지 센서 객체 생성
gas = DigitalInputDevice(17)

try:                                           # 무한 루프 시작 : 센서 상태를 계속 감시함
    while True:                                # 가스 감지 시 LOW(0) 신호 발생
        if gas.value == 0:                     # 가스 감지 센서에 가스가 감지 된다면
            print("gas gas")                   # gas gas 라는 메시지 0.2초 단위로 출력 + 부저 작동 O
            bz.on()
        else:
            print("True")                      # 가스 감지 센서에 가스가 감지 되지 않는다면
            bz.off()                           # True(정상 상태) 라는 메시지 0.2초 단위로 출력 + 부저 작동 X
            
        time.sleep(0.2)                        # 0.2초 쉼을 둔 이유 : 센서를 너무 자주 읽으면 CPU에 무리가 가므로 잠시 쉬어줌
        
except KeyboardInterrupt:                      # 사용자가 Ctrl + C 를 눌러 프로그램 강제종료 가능
    pass

bz.off()                                       # 프로그램이 종료될 때 부저가 켜져 있으면 안전하게 부저 끄기




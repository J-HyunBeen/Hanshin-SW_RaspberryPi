import paho.mqtt.client as mqtt
import time
from gpiozero import LED

# LED 핀 설정 (GPIO 번호)
greenLed = LED(16)
blueLed = LED(20)
redLed = LED(21)

# MQTT 메시지를 받았을 때 실행될 콜백 함수
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    
    # 페이로드 디코딩 후 메시지 내용 확인
    message = msg.payload.decode()
    print(message)
    
    # 메시지 값에 따라 각 LED On/Off 제어
    if message == "green_on":
        greenLed.on()
    elif message == "green_off":
        greenLed.off()
    elif message == "blue_on":
        blueLed.on()
    elif message == "blue_off":
        blueLed.off()
    elif message == "red_on":
        redLed.on()
    elif message == "red_off":
        redLed.off()

# MQTT 클라이언트 설정 및 콜백 등록
client = mqtt.Client()
client.on_message = on_message

# 브로커 연결 및 토픽 구독 (led 토픽, QoS 1)
broker_address = "172.30.1.90"
client.connect(broker_address)
client.subscribe("led", 1)

# 메시지 수신 대기를 위한 무한 루프
client.loop_forever()

import paho.mqtt.client as mqtt
import time
from gpiozero import LED

greenLed = LED(16)
blueLed = LED(20)
redLed = LED(21)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    message = msg.payload.decode()
    print(message)
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

client = mqtt.Client()
client.on_message = on_message

broker_address="172.30.1.90"
client.connect(broker_address)
client.subscribe("led",1)

client.loop_forever()

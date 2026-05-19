import requests
import os
import time

API_KEY = "Enter your API key here"
url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"

def speak(option, msg):
    os.system("espeak {} '{}'".format(option, msg))

try:
    while 1:
        response = requests.get(url)
        data = response.json()
        temp = data["main"]["temp"]
        humi = data["main"]["humidity"]

        msg = '    기온은 ' + str(int(temp)) + ' 도 습도는 ' + str(humi) + '퍼센트 입니다.'
        print(msg)
        option = '-s 180 -p 50 -a 200 -v ko+f5'
        speak(option, msg)
        time.sleep(10.0)

except KeyboardInterrupt:
    pass
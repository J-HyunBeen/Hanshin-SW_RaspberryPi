import urllib.request
import json

api_key = '48fde1e95a9d04732d98226e3be018a7'

url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"

with urllib.request.urlopen(url) as r:
    data = json.loads(r.read())

text = ""
for i in range(8):
    item = data['list'][i]
    hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)
    temp = item['main']['temp']
    humi = item['main']['humidity']
    desc = item['weather'][0]['description']
    text = text + "(" + str(hour) + "h "
    text = text + str(temp) + "C "
    text = text + str(humi) + "% "
    text = text + str(desc) + ")"

print(text)

import urllib.request
import json

api_key = '48fde1e95a9d04732d98226e3be018a7'

url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"

with urllib.request.urlopen(url) as r:
    data = json.loads(r.read())

time = [(int(item['dt_txt'][11:13]) + 9) % 24 for item in data['list']]
temp = [item['main']['temp'] for item in data['list']]
humi = [item['main']['humidity'] for item in data['list']]
desc = [item['weather'][0]['description'] for item in data['list']]

print(time)
print(temp)
print(humi)
print(desc)

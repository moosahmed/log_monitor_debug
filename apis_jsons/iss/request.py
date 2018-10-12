import requests
import json

param = {'lat': 38.8, 'lon': 122.3}

response = requests.get('http://api.open-notify.org/iss-pass.json', params=param)

print(response.status_code)
d = response.json()

print(d["response"][0]["duration"])
print(response.headers["CONTent-type"])

astros = requests.get('http://api.open-notify.org/astros.json')
print(astros.json()["number"])

(print(response.headers))

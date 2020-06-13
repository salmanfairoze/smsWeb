import urllib.request as urllib2
from urllib.request import urlopen
import time
import json

url = "https://api.covid19india.org/districts_daily.json"
response = urlopen(url)
data = json.loads(response.read())
print(data['districtsDaily']['Tamil Nadu']['Vellore'][-1])

flag = 0
for i in range(1, 28):
    if (data['districtsDaily']['Tamil Nadu']['Vellore'][-i]["active"] - data['districtsDaily']['Tamil Nadu']['Vellore'][-i-1]["active"] > 0):
        print("Orange Zone ")
        flag = 1
        break
if (flag == 0):
    print("Green Zone")
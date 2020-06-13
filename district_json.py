import urllib.request as urllib2
from urllib.request import urlopen
import time
import json

url = "https://api.covid19india.org/districts_daily.json"
response = urlopen(url)
data = json.loads(response.read())
print(data['districtsDaily']['Tamil Nadu']['Vellore'][-1])


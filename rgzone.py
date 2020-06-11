from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd
import re
from collections import OrderedDict

url="https://www.indiatoday.in/india/story/red-orange-green-zones-full-current-update-list-districts-states-india-coronavirus-1673358-2020-05-01#redgreenzonelisttn"
query = "Tamil Nadu"
soup = bs(urlopen(url),'lxml')
s=bs(urlopen(url),'lxml').decode('utf-8')
#print(soup)
x = re.findall("redgreenzonelist[a-zA-Z]*", s)
x=list(OrderedDict.fromkeys(x))
names=[]
for i in x:
	n=soup.findAll('a',attrs={'id':i,'name':i})
	n[0]=n[0].text
	names=names+n
							
print(names);

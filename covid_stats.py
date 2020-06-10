from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd

url="https://www.mohfw.gov.in"
query = "Karnataka"
soup = bs(urlopen(url),'lxml')
for table in soup.findAll('tbody'):
	row=table.findAll('tr')
	break;
sno=[]
name=[]
active=[]
cured_dis_mig=[]
deaths=[]
total_confirmed=[]
for col in row :
	c=col.findAll('td')
	if(len(c)==6):
		sno.append(c[0].text)
		name.append(c[1].text.lower())
		active.append(c[2].text)
		cured_dis_mig.append(c[3].text)
		deaths.append(c[4].text)
		total_confirmed.append(c[5].text)	
		
#print(name)
# print(sno)
df = pd.DataFrame({'sno':sno,'Name':name,"active":active,'Cured':cured_dis_mig,'deaths':deaths,"total_confirmed":total_confirmed}) 
# print(df)
print(df.loc[df['Name'] == query.lower()].to_string(index=False))
df.to_csv('cases.csv', index=False, encoding='utf-8')	

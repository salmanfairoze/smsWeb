from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
from bs4 import BeautifulSoup as bs
import time
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.covid19india.org/")
time.sleep(3)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
page = driver.page_source
soup = bs(page,'lxml')

row=soup.findAll('div', attrs={'class':'row'})

# state = "Mizoram"
# district = "Aizawl"

for i in range(1,len(row)):
	name=row[i].find('div', attrs={'class':'state-name'})

	if("Tamil Nadu"==name.text):

		print(name.text)
		j=i
		break

a=driver.find_elements_by_class_name("row")
time.sleep(3)
a[j].click()
time.sleep(3)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
page = driver.page_source
soup = bs(page,'lxml')
tot=row[j].findAll('div', attrs={'class':'total'})
print("confirmed:" ,tot[0].text,"active: ",tot[1].text,"Recovered: ",tot[2].text,"Dead: ",tot[3].text)
row=soup.findAll('div', attrs={'class':'row district'})
for k in row:

	if(k.find('div', attrs={'class':'state-name'}).text=='Vellore'):

		print(k.find('div', attrs={'class':'state-name'}).text)
		tot=k.findAll('div', attrs={'class':'total'})
		print("confirmed:",tot[0].text,"active: ",tot[1].text,"Recovered: ",tot[2].text,"Dead: ",tot[3].text)
		break



from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import pandas as pd
query="Tamil Nadu"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.covid19india.org/")
time.sleep(5)
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(5)
page = driver.page_source
soup = bs(page,'lxml')
for row in soup.findAll('div',attrs={'class':'row'}):
	cell=row.find('div', attrs={'class':'cell'})
	name=cell.find('div', attrs={'class':'state-name'})
	a=[]
	if name is not None:
		if(name.text==query):
			for stat in row.findAll('div',attrs={'class':'cell statistic'}):
				a.append(stat.find('div',attrs={'class':'total'}).text)
			print(name.text)
			print("confirmed",a[0])
			print("active",a[1])
			print("recovered",a[2])
			print("dead",a[3])
				
	
driver.quit()
time.sleep(2)
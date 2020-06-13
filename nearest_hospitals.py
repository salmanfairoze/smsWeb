from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
from bs4 import BeautifulSoup as bs
import time
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("http://www.google.com/maps/")
time.sleep(6)
driver.find_element_by_name("q").send_keys("Hospitals in Bidar")
driver.find_element_by_class_name("searchbox-searchbutton").click()
time.sleep(5)

for i in range(0,3):
	a=driver.find_elements_by_class_name("section-result")
	time.sleep(5)
	a[i].click()
	time.sleep(7)
	page = driver.page_source
	soup = bs(page,'lxml')

	cell=soup.findAll('div', attrs={'class':'ugiz4pqJLAG__primary-text gm2-body-2'})
	name=soup.find('h1', attrs={'class':'section-hero-header-title-title GLOBAL__gm2-headline-5'})
	
	print(name.text)
	for k in range(0,len(cell)-1):
		if(k!=1):
			print(cell[k].text)
	op=soup.findAll('span', attrs={'class':'cX2WmPgCkHi__section-info-text cX2WmPgCkHi__red'})
	

	for l in op:
		print(l.text);
	op1=soup.findAll('span', attrs={'class':'cX2WmPgCkHi__section-info-text'})
	for l in op1:
		print(l.text);
		
	print('')
	time.sleep(5)
	driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/button").click()
	time.sleep(3)
	
driver.quit()
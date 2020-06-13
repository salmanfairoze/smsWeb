from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup as bs
import html2text
import time
# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.get("http://www.google.com/maps/")
# time.sleep(6)
# driver.find_element_by_name("q").send_keys("Hospitals in banashankari")
# driver.find_element_by_class_name("searchbox-searchbutton").click()
# time.sleep(10)
# page = driver.page_source

query = "hospital+in+banashankari"
url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
req = Request(url, headers = headers)
page =urlopen(req)
html_content = page.read().decode('utf-8')
print(html_content)

# print(page)
h = html2text.HTML2Text()
h.ignore_images = True
h.ignore_emphasis = True
h.escape_all = True
soup = bs(html_content, 'lxml')
text_content = soup.findAll("div", attrs={"class":"section-result-text-content"})
print(text_content)
string = ""
for i in range(0, 5):
	title_parent = text_content[i].find("h3", attrs={"class":"section-result-title"})
	title_tag = title_parent.find("span")
	title = title_tag.contents
	location_tag = text_content[i].find("span", attrs={"class":"section-result-location"})
	location = location_tag.contents
	details = text_content[i].find("div", attrs={"class":"section-result-hours-phone-container"})
	details_text = h.handle(str(details)).encode('utf-8')
	print(title, location, details_text)
	
# rendered_content = h.handle(string).encode('utf-8')
# print(rendered_content)
# for i in range(0,3):
# 	a=driver.find_elements_by_class_name("section-result")
# 	time.sleep(5)
# 	a[i].click()
# 	time.sleep(7)
# 	page = driver.page_source
# 	soup = bs(page,'lxml')

# 	cell=soup.findAll('div', attrs={'class':'ugiz4pqJLAG__primary-text gm2-body-2'})
# 	name=soup.find('h1', attrs={'class':'section-hero-header-title-title GLOBAL__gm2-headline-5'})
	
# 	print(name.text)
# 	for k in range(0,len(cell)-1):
# 		if(k!=1):
# 			print(cell[k].text)
# 	op=soup.findAll('span', attrs={'class':'cX2WmPgCkHi__section-info-text cX2WmPgCkHi__red'})
	

# 	for l in op:
# 		print(l.text);
# 	op1=soup.findAll('span', attrs={'class':'cX2WmPgCkHi__section-info-text'})
# 	for l in op1:
# 		print(l.text);
		
# 	print('')
# 	time.sleep(5)
# 	driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/button").click()
# 	time.sleep(3)
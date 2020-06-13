from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
from bs4 import BeautifulSoup as bs
import time
#input is location you want to find . It returns a string	
def location(query):
	
	flag1=0
	while(flag1==0):
		driver = webdriver.Chrome(ChromeDriverManager().install())
		##print("hi");
		driver.get("http://www.google.com/maps/")
		time.sleep(2)
		try:
			##print("hi2");
			q=driver.find_element_by_name("q")
		
			q.send_keys(query)
			flag1=1
			##print("hi3");
			sb=driver.find_element_by_class_name("searchbox-searchbutton")
			##print("hi4")
			sb.click()
			##print("hi5")
			time.sleep(5)
			g=driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div/button/span[1]")
			
			
			if(g is None):
				flag1=0
			else:
				flag1=1
				##print(g,"g")
		except:
			flag1=0
			
	ans=""
	for i in range(0,3):
		flag2=0
		while(flag2==0):
			##print("h2");
			try:
				a=driver.find_elements_by_class_name("section-result")
				time.sleep(5)
				##print("httttt ccccc")
				a[i].click()
				##print("httttt")
				time.sleep(6)
				##print("h")
				h=driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[5]/div[1]/div/button")
				if(h is None):
					flag2=0
				else:
					##print(h,"h")
					flag2=1
				
			except:
				flag2=0
		
			flag3=0
			while(flag2==1 and flag3==0):
				##print("h3");
				try:
					page = driver.page_source
					soup = bs(page,'lxml')
					##print("h31");
					cell=soup.findAll('div', attrs={'class':'ugiz4pqJLAG__primary-text gm2-body-2'})
					name=soup.find('h1', attrs={'class':'section-hero-header-title-title GLOBAL__gm2-headline-5'})
					##print("h32");
					#print(name.text)
					ans=ans+name.text+"\n"
					for k in range(0,len(cell)-1):
						if(k!=1):
							#print(cell[k].text)
							ans=ans+cell[k].text+"\n"
					op=soup.findAll('span', attrs={'class':'cX2WmPgCkHi__section-info-text cX2WmPgCkHi__red'})
					##print("h56");

					for l in op:
						#print(l.text);
						ans=ans+l.text+"\n"
					op1=soup.findAll('span', attrs={'class':'cX2WmPgCkHi__section-info-text'})
					for l in op1:
						#print(l.text);
						ans=ans+l.text+"\n"
					##print("h55");	
					ans=ans+"\n\n"
					time.sleep(2)
					flag4=0
					##print("pranav");
					flag3=1
					while(flag3==1 and flag4==0):
						##print("h4");
						try:
							driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/button").click()
							time.sleep(3)
							flag4=1
						except:
							flag4=0
					
				except:
					##print("except in 3")
					flag3=0
	driver.quit()
	return ans	
#input is location you want to find . It returns a string		

'''
q="Hospitals in banashankari"

ans=location(q)
print(ans)
'''

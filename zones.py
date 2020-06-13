import urllib.request as urllib2
from urllib.request import urlopen
from urllib.request import Request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

def calculate_cases(query):
	url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
	req = Request(url, headers = headers)
	page =urlopen(req)
	# page = urllib2.urlopen(url)
	html_content = page.read().decode('utf-8')

	soup = BeautifulSoup(html_content, 'lxml')
	div_tag = soup.find("div", attrs={"class":'SPZz6b'})
	span_tag = div_tag.findAll("span")
	temp_state = span_tag[1].contents[0].split(" ")[2:]

	state = " ".join(temp_state)
	district = span_tag[0].contents[0]
	#print(state, district)

	
	flag1=0
	while(flag1==0):
		try:
			driver = webdriver.Chrome(ChromeDriverManager().install())
			driver.get("https://www.covid19india.org/")
			time.sleep(3)
			driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
			page = driver.page_source
			soup = BeautifulSoup(page,'lxml')
			flag1=1
		except:
			flag1=0
		##print("hiiiiii111111")
		row=soup.findAll('div', attrs={'class':'row'})

		for i in range(1,len(row)):
		    name=row[i].find('div', attrs={'class':'state-name'})
		    if(state in name.text):
		        # #print(name.text)
		        j=i
		        break
		flag2=0
		while(flag1==1 and flag2==0):
			try:
				a=driver.find_elements_by_class_name("row")
				time.sleep(3)
				a[j].click()
				time.sleep(3)
				driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
				flag2=1
				page = driver.page_source
				soup = BeautifulSoup(page,'lxml')
				tot=row[j].findAll('div', attrs={'class':'total'})
				active_district = -1
				active_state = -1
				confirmed_state = tot[0].text
				active_state = tot[1].text
				recovered_state = tot[2].text
				dead_state = tot[3].text
				##print("hiiiiii")
				# #print("confirmed:" , confirmed_state, "active: ", active_state, "Recovered: ", recovered_state, "Dead: ", dead_state)
				row=soup.findAll('div', attrs={'class':'row district'})
				for k in row:
					if(district in k.find('div', attrs={'class':'state-name'}).text):
						# #print(k.find('div', attrs={'class':'state-name'}).text)
						tot=k.findAll('div', attrs={'class':'total'})
						confirmed_district = tot[0].text
						active_district = tot[1].text
						recovered_district = tot[2].text
						dead_district = tot[3].text
						# #print("confirmed:", confirmed_district, "active: ", active_district, "Recovered: ", recovered_district, "Dead: ", dead_district)
						active_district = active_district.replace(",", "")
						break
				
				active_state = active_state.replace(",", "")
				if (active_district != -1):
					percentage_wrt_state = ((int(active_district) / int(active_state)) * 100)
					if (percentage_wrt_state >= 0.8):
						zone = "RED ZONE"
						# #print("RED ZONE")
					else:
						url = "https://api.covid19india.org/districts_daily.json"
						response = urlopen(url)
						data = json.loads(response.read())
						# #print(data['districtsDaily'][state][district][-1])

						flag = 0
						for i in range(1, 28):
						    if (data['districtsDaily'][state][district][-i]["active"] - data['districtsDaily'][state][district][-i-1]["active"] > 0):
						        zone = "ORANGE ZONE"
						        # #print("Orange Zone ")
						        flag = 1
						        break
						if (flag == 0):
						    zone = "GREEN ZONE"
					# #print(zone, active_state, active_district, confirmed_state, confirmed_district, recovered_state, recovered_district)
					res = zone + '\n' + "District - " + district + '\n\t- ' + str(active_district) + " - Active Cases" + "\n\t- " + str(confirmed_district) + " - Confirmed Cases" + "\n\t- " + str(recovered_district) + " - Recovered Cases" + "\n" + str(percentage_wrt_state) + " Percentage of active cases wrt State" + "\n" + "State - " + state + "\n\t- " + str(active_state) + " - Active Cases" + "\n\t- " + str(confirmed_state) + " - Confirmed Cases" + "\n\t- " + str(recovered_state) + " - Recovered Cases"
					#print(res)
					return res 
				else:
					#print("It is not a District")
					res="It is not a District"
					return res
			except:
				flag2=0
'''
district = "Rupnagar"
result = calculate_cases(district)
print(result)
'''

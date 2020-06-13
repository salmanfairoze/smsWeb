import urllib.request as urllib2
from urllib.request import urlopen
from urllib.request import Request
import html2text
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

def calculate_cases(state, district):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.covid19india.org/")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    page = driver.page_source
    soup = BeautifulSoup(page,'lxml')

    row=soup.findAll('div', attrs={'class':'row'})

    # state = "Mizoram"
    # district = "Aizawl"

    for i in range(1,len(row)):
        name=row[i].find('div', attrs={'class':'state-name'})
        if(state in name.text):
            print(name.text)
            j=i
            break

    a=driver.find_elements_by_class_name("row")
    time.sleep(3)
    a[j].click()
    time.sleep(3)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    page = driver.page_source
    soup = BeautifulSoup(page,'lxml')
    tot=row[j].findAll('div', attrs={'class':'total'})
    active_district = -1
    active_state = -1
    confirmed_state = tot[0].text
    active_state = tot[1].text
    recovered_state = tot[2].text
    dead_state = tot[3].text
    print("confirmed:" , confirmed_state, "active: ", active_state, "Recovered: ", recovered_state, "Dead: ", dead_state)
    row=soup.findAll('div', attrs={'class':'row district'})
    for k in row:
        if(district in k.find('div', attrs={'class':'state-name'}).text):
            print(k.find('div', attrs={'class':'state-name'}).text)
            tot=k.findAll('div', attrs={'class':'total'})
            confirmed_district = tot[0].text
            active_district = tot[1].text
            recovered_district = tot[2].text
            dead_district = tot[3].text
            print("confirmed:", confirmed_district, "active: ", active_district, "Recovered: ", recovered_district, "Dead: ", dead_district)
            active_district = active_district.replace(",", "")
            break
    
    active_state = active_state.replace(",", "")
    if (active_district != -1):
        percentage_wrt_state = (int(active_district) / int(active_state))
        if (percentage_wrt_state >= 0.8):
            print("RED ZONE")
        else:
            url = "https://api.covid19india.org/districts_daily.json"
            response = urlopen(url)
            data = json.loads(response.read())
            print(data['districtsDaily'][state][district][-1])

            flag = 0
            for i in range(1, 28):
                if (data['districtsDaily'][state][district][-i]["active"] - data['districtsDaily'][state][district][-i-1]["active"] > 0):
                    print("Orange Zone ")
                    flag = 1
                    break
            if (flag == 0):
                print("Green Zone")
            print(percentage_wrt_state)
    else:
        print("It is not a District")

def get_zone(query):
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
    print(state, district)
    calculate_cases(state, district)


# Input
query = "ramanagara"

get_zone(query)

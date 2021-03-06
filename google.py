import urllib.request as urllib2
from urllib.request import urlopen
from urllib.request import Request
import html2text

from bs4 import BeautifulSoup

# sms based arogyasetu
# Help bot
# test centers
# Symtom check
# Track and untrack
# cellphone tower triangulation

# sms proxy
# health bot
# education bot
# try to attach the api

# business viability to the education, 
# law and order, helath care, finance, environment, agriculture, jobs, 

query = "worldlargestcountry"
url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
req = Request(url, headers = headers)
page =urlopen(req)
html_content = page.read().decode('utf-8')

file_google = open('google.txt', 'w')
file_google.write(html_content)
file_google.close()
# print(html_content)
"""
soup = BeautifulSoup(html_content, 'lxml')
content = soup.prettify()
# All the contents will be inside this div
content_div = soup.find("div", attrs={"class":"mw-parser-output"})
string = ""
table_contents = {}
for i in content_div.contents:
    # This contains the div of links
    nn_sibling = i.nextSibling.nextSibling
    if((i.name == "p") and (i.contents[0] != '\n') and (nn_sibling.name == "div")):
        string += str(i)
        if (nn_sibling["id"] == "toc"):
            links = str(nn_sibling)
            ul = nn_sibling.findAll("ul")
            for j in ul:
                span = j.findAll("span")
                length_span = len(span)
                # Get the Number and Reference
                for k in range(0, length_span, 2):
                    key = span[k].contents
                    value = span[k+1].contents
                    val = value[0].replace(' ', '_')
                    table_contents[key[0]] = val
        break
    # Gets the starting paragraph
    elif((i.name == "p") and (i.contents[0] != '\n')):
        string += str(i)

# This query_2 is the query to the link i.e.,
#    it is contained in the table_contents dictionary
query_2 = '1'
req_res = table_contents[query_2]
find = soup.find(id=req_res)
# Position of the Reference LInk
link_extract = find.parent.nextSibling.nextSibling

if (link_extract.name == "div"):
    link_extract = link_extract.nextSibling.nextSibling

li = list(table_contents)
# to get the next link in the dict
res = li[li.index(query_2)+1]

next_target = soup.find(id=table_contents[res])

link_extract_str = str(link_extract)
if (link_extract != next_target.parent):
    temp = link_extract.nextSibling

    # to get all the data till the next link
    while(temp != next_target.parent):
        link_extract_str += str(temp)
        temp = temp.nextSibling
        


h = html2text.HTML2Text()
h.ignore_images = True
h.ignore_emphasis = True
h.escape_all = True
rendered_content = h.handle(string).encode('utf-8')
link_content = h.handle(links).encode('utf-8')
link_extract = h.handle(link_extract_str).encode('utf-8')

# File which contains the Starting Paragraph of the Wiki page
file = open('wiki_text.txt', 'w')
file.write(rendered_content.decode('utf-8'))
file.close()

# File which contains the Respective links with numbers
file_link = open('link_text.txt', 'w')
file_link.write(link_content.decode('utf-8'))
file_link.close()

# File which contains the Target data of the link
file_link_extract = open('link_extract.txt', 'w')
file_link_extract.write(link_extract.decode('utf-8'))
file_link_extract.close()
"""
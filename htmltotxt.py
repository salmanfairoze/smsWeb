import urllib2
from urllib2 import urlopen
from urllib2 import Request
import html2text
query = "Worlds smallest country"
url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
req = urllib2.Request(url, headers = headers)
page = urllib2.urlopen(req)
# page = urllib2.urlopen(url)
html_content = page.read().decode('utf-8')
h = html2text.HTML2Text()
h.ignore_images = True
h.ignore_emphasis = True
h.escape_all = True
rendered_content = h.handle(html_content).encode('utf-8')
file = open('file_text.txt', 'w')
file.write(rendered_content)
file.close()
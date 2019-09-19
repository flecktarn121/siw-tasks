import sys
import requests
import time
from bs4 import BeautifulSoup

urls = []
visitedPages = {}

urlFile = sys.argv[1]
maxFiles = sys.argv[2]
waitingTime = 10 

def getUrl(filename):
    file = open(filename, "r")
    lines = file.read().splitlines()
    for line in lines:
        urls.append(line)
    file.close()

def crawl(url, seconds, numberOfLinks):
    if url in visitedPages:
        return
    else:
        visitedPages[url] = ""
    if numberOfLinks == 0:
        return
    #else:
        #numberOfLinks -= 1
    html = download(url)
    if len(html) == 0:
        return
    soup = BeautifulSoup(html)
    file = open(soup.title.string+'html', 'w+')
    file.write(html)
    file.close()
    #discard all elements except the ones with the <a> tag
    for link in soup.find_all('a', href = True):
        #get the href attribute of the html tag
        crawl(link['href'], seconds, numberOfLinks)
        #TODO: check if the link is a subdomain

def download(url):
    request = requests.get(url)
    if "text/html" in request.headers["content-type"]:
        return ""
    return request.text

getUrl(urlFile)
for url in urls:
    crawl(url, waitingTime, maxFiles)

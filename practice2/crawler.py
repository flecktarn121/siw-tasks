import sys
import requests
import time
from bs4 import BeautifulSoup
import urllib.parse

urls = []
visitedPages = {}

urlFile = sys.argv[1]
maxFiles = int(sys.argv[2]) 
waitingTime = int(sys.argv[3])

class Crawler:
    def __init(self, url, maxFiles, seconds):
        self.url = url
        self.maxFiles = maxFiles
        self.seconds = seconds
        def getUrl(filename):
            file = open(filename, "r")
            lines = file.read().splitlines()
            for line in lines:
                urls.append(line)
            file.close()

        def crawl(url, seconds):
            global maxFiles
            if url == "":
                return
            if url in visitedPages:
                return
            else:
                visitedPages[url] = ""
            if maxFiles < 1:
                return
            else:
                maxFiles -= 1
            html = download(url)
            if html == "":
                return
            soup = BeautifulSoup(html, features="html.parser")
            print("Saving " + url + "...")
            print("Remaining pages: "+ str(maxFiles))
            file = open(soup.title.string.replace("/","|")+'.html', 'w+')
            file.write(html)
            file.close()
            #discard all elements except the ones with the <a> tag
            for link in soup.find_all('a', href = True):
                #get the href attribute of the html tag
                l = normalizeLink(url, link["href"])
                crawl(l, seconds) 

        def normalizeLink(url, link):
            if link.startswith("/") or link.startswith("#") or link.startswith("../"):
                return urllib.parse.urljoin(url, link)
            else:
                return link

        def download(url):
            request = requests.get(url)
            if "text/html" in request.headers["content-type"]:
                return request.text
            else:
                return ""


def getUrl(filename):
    file = open(filename, "r")
    lines = file.read().splitlines()
    for line in lines:
        urls.append(line)
    file.close()

def crawl(url, seconds):
    global maxFiles
    if url == "":
        return
    if url in visitedPages:
        return
    else:
        visitedPages[url] = ""
    if maxFiles < 1:
        return
    else:
        maxFiles -= 1
    html = download(url)
    if html == "":
        return
    soup = BeautifulSoup(html, features="html.parser")
    print("Saving " + url + "...")
    print("Remaining pages: "+ str(maxFiles))
    file = open(soup.title.string.replace("/","|")+'.html', 'w+')
    file.write(html)
    file.close()
    #discard all elements except the ones with the <a> tag
    for link in soup.find_all('a', href = True):
        #get the href attribute of the html tag
        l = normalizeLink(url, link["href"])
        crawl(l, seconds) 

def normalizeLink(url, link):
    if link.startswith("/") or link.startswith("#") or link.startswith("../"):
        return urllib.parse.urljoin(url, link)
    else:
        return link

def download(url):
    request = requests.get(url)
    if "text/html" in request.headers["content-type"]:
        return request.text
    else:
        return ""

getUrl(urlFile)
for url in urls:
    crawl(url, waitingTime)
    maxFiles = 10

import sys
import requests
import time
from bs4 import BeautifulSoup
import urllib.parse

urls = []

urlFile = sys.argv[1]
maxFiles = int(sys.argv[2]) 
waitingTime = int(sys.argv[3])

class Crawler:
    def __init__(self, url, maxFiles, seconds): 
        print("Initializing crawler for " + url)
        self.visitedPages = {}
        self.url = url
        self.maxFiles = maxFiles
        self.seconds = seconds
        self.html = ""

    def crawl(self): 
        if not self.isCrawlable():
            return
        soup = BeautifulSoup(self.html, features="html.parser")
        print("Saving " + self.url + "...")
        print("Remaining pages: "+ str(self.maxFiles))
        self.writeHtml(soup, self.html)
        time.sleep(waitingTime)
        #discard all elements except the ones with the <a> tag
        for link in soup.find_all('a', href = True):
            #get the href attribute of the html tag
            l = self.normalizeLink(self.url, link["href"])
            self.url = l
            self.crawl() 
    
    def isCrawlable(self):
        if self.url == "":
            return False
        if self.url in self.visitedPages:
            return False
        if self.maxFiles < 1:
            return False
        self.html = self.download(self.url)
        if self.html == "":
            return False
        self.visitedPages[self.url] = ""
        self.maxFiles -= 1
        return True

    def writeHtml(self, soup, html):
        file = open(soup.title.string.replace("/","|")+'.html', 'w+')
        file.write(html)
        file.close()
    
    def normalizeLink(self, url, link):
        # In case it is a partial link, make it absolute
        if link.startswith("/") or link.startswith("#") or link.startswith("../"):
            return urllib.parse.urljoin(url, link)
        else:
            return link

    def download(self, url):
        request = requests.get(url)
        # Make sure it is an html        
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

getUrl(urlFile)

for url in urls:
    crawler = Crawler(url, maxFiles, waitingTime)
    crawler.crawl()

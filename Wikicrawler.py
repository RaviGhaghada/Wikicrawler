import urllib.request
import lxml.html
import time
from queue import Queue


class Wikicrawler:

    def __init__(self, start, end):
        self.visted = {}
        self.tovisit = Queue()

        self.STARTURL = start
        self.ENDURL = end
        self.BASEURL = "https://en.wikipedia.org{}"

        self.tovisit.put(self.STARTURL)

    def crawlURL(self):

        currURL = self.tovisit.get()
        self.visted[currURL] = " "

        connection = urllib.request.urlopen(self.BASEURL.format(currURL))
        dom = lxml.html.fromstring(connection.read())

        for link in dom.xpath('//a/@href'):  # select the url in href for all a tags(links)
            if self.isAcceptableFormat(link):
                if not self.hasBeenEncountered(link):
                    print("\n" + link)
                    if link == self.ENDURL:
                        print("\nEND URL Reached!")
                        return True
                    self.tovisit.put(link)
        return False

    def main(self):
        while not self.tovisit.empty():
            self.crawlURL()

    def isAcceptableFormat(self, link):
        link = str(link)

        if not link.startswith("/wiki/"):
            return False
        if "/Wikipedia:" in link:
            return False
        if "/Category:" in link:
            return False
        if "/Special:" in link:
            return False
        if "/Talk:" in link:
            return False

        return True

    def hasBeenEncountered(self, link):
        link = str(link)
        if link in self.visted:
            return True
        if link in self.tovisit.queue:
            return True
        return False



a = Wikicrawler("/wiki/Tom_Scott_(entertainer)", "/wiki/London")
while not a.crawlURL():
    pass
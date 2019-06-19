import urllib.request
import lxml.html
import time
from queue import Queue


class Wikicrawler:

    def __init__(self, start, end):
        self.visited = {}
        self.tovisit = Queue()

        self.STARTURL = start
        self.ENDURL = end
        self.BASEURL = "https://en.wikipedia.org{}"

        self.tovisit.put(self.STARTURL)

    def crawlURL(self):

        currURL = self.tovisit.get()

        connection = urllib.request.urlopen(self.BASEURL.format(currURL))
        dom = lxml.html.fromstring(connection.read())

        for link in dom.xpath('//a/@href'):  # select the url in href for all a tags(links)
            if self.is_acceptable_format(link):
                if not self.has_been_encountered(link):
                    print("\n" + link)

                    self.visited[link] = currURL

                    if link == self.ENDURL:
                        print("\nEND URL Reached!")
                        return self.count_retrace(link)
                    self.tovisit.put(link)
        return 0

    def is_acceptable_format(self, link):
        link = str(link)

        badwords = ["/Wikipedia:", "/Category:", "/Special:", "/Talk:", "/File:",
                    "/Template", "/Template_talk:", "/Help:", "/Portal:", "/Book:"]

        if not link.startswith("/wiki/"):
            return False

        for i in badwords:
            if i in link:
                return False

        return True

    def has_been_encountered(self, link):
        link = str(link)
        if link in self.visited:
            return True
        return False

    def count_retrace(self, link):
        if link == self.STARTURL:
            return 0
        else:
            return 1 + self.count_retrace(self.visited[link])



a = Wikicrawler("/wiki/Planet", "/wiki/Divinity")
while True:
    result = a.crawlURL()
    if result !=0:
        print(result)
        break

from xml.dom import minidom
from html.parser import HTMLParser

class PuckDnsParser(HTMLParser):
    """Help util to find 'DOM part' of response"""
    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.tableStart = self.getpos()[1]
        elif tag == "span":
            if attrs == [('id', 'error'), ('class', 'error')]:
                errorStart = self.getpos()[1] + len ('<span id="error" class="error">')
                self.errormsg = self.rawdata[errorStart:self.rawdata.find("</span>", errorStart)]
            elif attrs == [('id', 'message'), ('class', 'message')]:
                msgStart = self.getpos()[1] + len('<span id="message" class="message">')
                self.infomsg = self.rawdata[msgStart:self.rawdata.find("</span>", msgStart)]

    def handle_endtag(self, tag):
        if tag == "table":
            self.table = minidom.parseString(self.rawdata[self.tableStart:self.getpos()[1] + len("</table>")])

import requests
from xml.dom import minidom
from html.parser import HTMLParser


class _MyParser(HTMLParser):
    """Help util to find 'DOM part' of response"""
    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.start = self.getpos()[1]

    def handle_endtag(self, tag):
        if tag == "table":
            self.stop = self.getpos()[1] + len("</table>")


class API():
    """API for working with puck.nether.net/dns"""

    def login(self, username, password):
        self.r = requests.post("https://puck.nether.net/dns/login", data={'username': username, 'password': password})
        assert self.r.url == 'https://puck.nether.net/dns/dnsinfo', "[FATAL] Login Failed"
        self.cookies = self.r.cookies
        self.loggedIn = True

    def logout(self):
        if self.loggedIn:
            self._logout()

    def _logout(self):
        self.r = requests.get("https://puck.nether.net/dns/logout", cookies=self.cookies)
        self.loggedIn = False
        del self.cookies

    def __runTests(self):
        assert self.loggedIn, "Please login first"

    def get_DNS_Info_TD(self):
        self.__runTests()
        self.r = requests.get("https://puck.nether.net/dns/dnsinfo", cookies=self.cookies)

        text = self.r.text.replace("\n", "")
        parser = _MyParser()
        parser.feed(text)
        dom = minidom.parseString(text[parser.start:parser.stop])
        return dom.getElementsByTagName("td")

    def getDomains(self):
        tdList = self.get_DNS_Info_TD()
        return [tdList[i].firstChild.data for i in range(len(tdList)) if i%7 == 2] #from 7 fields in able the 3rd one -> 0,1,2

    def set_IP (self, domain, ip):
        self.__runTests()
        self.data = {"domainname": domain, "masterip": ip, "aa": "Y", "submit": "Submit"}
        self.r = requests.post("https://puck.nether.net/dns/dnsinfo/edit/" + domain, data=self.data, cookies=self.cookies)

    def get_IP(self, domain):
        tdList = self.get_DNS_Info_TD()
        return [tdList[i+1].firstChild.data for i in range(len(tdList)) if i%7 == 2 and
                tdList[i].firstChild.data == domain]

    def setAllIP(self, ip):
        for domain in self.getDomains():
            self.set_IP(domain, ip)


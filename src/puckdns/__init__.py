import requests
from .puckdnsExceptions import *
from .puckDnsParser import PuckDnsParser

class API():
    """API for working with https://puck.nether.net/dns"""

    __loggedIn = False
    url = "https://puck.nether.net/dns/dnsinfo"
    cookies = ""

    def login(self, username, password):
        """Login to puck dns service with given username and password"""
        self.r = requests.post("https://puck.nether.net/dns/login", data={'username': username, 'password': password})
        if self.r.url != 'https://puck.nether.net/dns/dnsinfo':
            raise LoginFailed(username)
        self.cookies = self.r.cookies
        self.__loggedIn = True
        self.__username = username
        self.__pwd = password
    
    def isLoggedIn(self):
        return self.__loggedIn

    def logout(self):
        """Logout from puck dns service"""
        if self.__loggedIn:
            self._logout()

    def _logout(self):
        """Force logout from puck dns service"""
        self.r = requests.get("https://puck.nether.net/dns/logout", cookies=self.cookies)
        self.__loggedIn = False
        del self.cookies

    def __runTests (self):
        """Check preconditions like successful login before performing requests to puck dns service"""
        if not self.__loggedIn:
            raise NotLoggedIn()

    def __makeGetRequest(self, location, expectedMsg):
        self.__runTests()
        
        url = self.url + location
        self.r = requests.get(url, cookies=self.cookies)
        if self.r.url == "https://puck.nether.net/dns/login":
            self.login(self.__username, self.__pwd)
            self.r = requests.get(url, cookies=self.cookies)
        parser = PuckDnsParser()
        parser.feed(self.r.text.replace("\n", ""))
        if parser.errormsg != '':
            raise PuckDnsError(expectedMsg, parser.errormsg, url)
        if parser.infomsg != expectedMsg:
            raise PuckDnsWrongMsg(expectedMsg, parser.infomsg, url)
        return parser
        
    def __makePostRequest(self, location, payload, expectedMsg):
        self.__runTests()
        
        url = self.url + location
        self.r = requests.post(url, data=payload, cookies=self.cookies)
        if self.r.url == "https://puck.nether.net/dns/login":
            self.login(self.__username, self.__pwd)
            self.r = requests.post(url, data=payload, cookies=self.cookies)
        parser = PuckDnsParser()
        parser.feed(self.r.text.replace("\n", ""))
        if parser.errormsg != '':
            raise PuckDnsError(expectedMsg, parser.errormsg, url)
        if parser.infomsg != expectedMsg:
            raise PuckDnsWrongMsg(expectedMsg, parser.infomsg, url)
        return parser

    def get_DNS_Info_TD (self):
        """Returns extracted table data from puck dns service"""
        parser = self.__makeGetRequest("", "")
        return parser.table.getElementsByTagName("td")

    def getDomains (self):
        """Returns registered domains from puck dns service"""
        tdList = self.get_DNS_Info_TD()
        return [tdList[i].firstChild.data for i in range(len(tdList)) if i%7 == 2] #from 7 fields in able the 3rd one -> 0,1,2

    def set_IP (self, domain, ip):
        """Sets IP address for specific domains from puck dns service"""
        payload = {"domainname": domain, "masterip": ip, "aa": "Y", "submit": "Submit"}
        self.__makePostRequest(f"/edit/{domain}", payload, "Domain successfully edited.")

    def get_IP (self, domain):
        """Gets IP address for specific domains from puck dns service"""
        tdList = self.get_DNS_Info_TD()
        return [tdList[i+1].firstChild.data for i in range(len(tdList)) if i%7 == 2 and
                tdList[i].firstChild.data == domain]

    def setAllIP (self, ip):
        """Set same master IP address for all domains registered at puck dns service with this user account"""
        for domain in self.getDomains():
            self.set_IP(domain, ip)
    
    def addDomain (self, ip, domain):
        """Add domain to puck DNS"""
        payload = {"domainname": domain, "masterip": ip, "submit": "Submit"}
        self.__makePostRequest("/add", payload, "Inserted new domain.")

    def addDomains (self, ip, domainsList):
        """Add multiple domain entries at once"""
        data = {"domains": "\n".join(domainsList), "masterip": ip, "submit": "Submit"}
        self.__makePostRequest("/bulk_add", data, "Domains inserted.")

    def delDomain(self, domain):
        """Delete domain from puck DNS"""
        self.__makeGetRequest(f"/delete/{domain}", f"{domain} successfully removed.")

    def delDomains(self, domainList):
        """Delete Multiple Domains"""
        for domain in domainList:
            self.delDomain(domain)

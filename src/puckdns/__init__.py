from urllib import request
from urllib.parse import urlencode
from http.cookiejar import CookieJar
from .puckdnsExceptions import *
from .puckDnsParser import PuckDnsParser

class API():
    """API for working with https://puck.nether.net/dns"""

    __loggedIn = False
    __cookiejar = CookieJar()
    __HTTPRequestHandler = request.build_opener(request.HTTPCookieProcessor(__cookiejar))
    url = "https://puck.nether.net/dns/dnsinfo"

    def login(self, username, password):
        """Login to puck dns service with given username and password"""

        req = request.Request("https://puck.nether.net/dns/login", urlencode({'username': username, 'password': password, 'submit':'Login'}).encode())
        with self.__HTTPRequestHandler.open(req) as answer:
            if answer.url != 'https://puck.nether.net/dns/dnsinfo':
                raise LoginFailed(username)
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
        req = request.Request("https://puck.nether.net/dns/logout")
        self.__HTTPRequestHandler.open(req)
        self.__loggedIn = False

    def __runTests (self):
        """Check preconditions like successful login before performing requests to puck dns service"""
        if not self.__loggedIn:
            raise NotLoggedIn()
    
    def __makeRequest(self, location, expectedMsg, payload=None):
        self.__runTests()
        
        url = self.url + location
        if payload:
            req = request.Request(url, urlencode(payload).encode())
        else:
            req = request.Request(url)
        answer = self.__HTTPRequestHandler.open(req)
        if answer.url == "https://puck.nether.net/dns/login":
            self.login(self.__username, self.__pwd)
            answer = self.__HTTPRequestHandler(req)
        parser = PuckDnsParser()
        parser.feed(answer.read().decode().replace("\n", ""))
        if parser.errormsg != '':
            raise PuckDnsError(expectedMsg, parser.errormsg, url)
        if parser.infomsg != expectedMsg:
            raise PuckDnsWrongMsg(expectedMsg, parser.infomsg, url)
        return parser

    def get_DNS_Info_TD (self):
        """Returns extracted table data from puck dns service"""
        parser = self.__makeRequest("", "")
        return parser.table.getElementsByTagName("td")

    def getDomains (self):
        """Returns registered domains from puck dns service"""
        tdList = self.get_DNS_Info_TD()
        return [tdList[i].firstChild.data for i in range(len(tdList)) if i%7 == 2] #from 7 fields in able the 3rd one -> 0,1,2

    def set_IP (self, domain, ip):
        """Sets IP address for specific domains from puck dns service"""
        payload = {"domainname": domain, "masterip": ip, "aa": "Y", "submit": "Submit"}
        self.__makeRequest(f"/edit/{domain}", "Domain successfully edited.", payload)

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
        self.__makeRequest("/add", "Inserted new domain.", payload)

    def addDomains (self, ip, domainsList):
        """Add multiple domain entries at once"""
        data = {"domains": "\n".join(domainsList), "masterip": ip, "submit": "Submit"}
        self.__makeRequest("/bulk_add", "Domains inserted.", data)

    def delDomain(self, domain):
        """Delete domain from puck DNS"""
        self.__makeRequest(f"/delete/{domain}", f"{domain} successfully removed.")

    def delDomains(self, domainList):
        """Delete Multiple Domains"""
        for domain in domainList:
            self.delDomain(domain)

class NotLoggedIn (Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Call puckdns.API.login(<username>, <password>) to login to the puck dns server"

class LoginFailed(Exception):
    def __init__(self, username):
        self.__username = username
    def __str__(self):
        return f"(Re)login to puck dns service failed.\nPlease check ur user credentials giving to user: {self.__username}."

class PuckDnsError(Exception):
    def __init__(self, expectedMsg, recvMsg, url):
        self.__expectedMsg = expectedMsg
        self.__recvMsg = recvMsg
        self.__url = url
    def __str__(self):
        return f"Error during call of {self.__url}.\nPuck dns service throws following error:\n\'{self.__recvMsg}\'.\nExpected Message: \'{self.__expectedMsg}\'"

class PuckDnsWrongMsg(Exception):
    def __init__(self, expectedMsg, recvMsg, url):
        self.expectedMsg = expectedMsg
        self.recvMsg = recvMsg
        self.url = url
    def __str__(self):
        return f"Wrong behavior from puck dns service during call of '{self.url}\':\n Excepted Message: \'{self.expectedMsg}\'\nGot: \'{self.recvMsg}\'"

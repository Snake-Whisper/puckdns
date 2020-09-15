class NotLoggedIn (Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Call puckdns.API.login(<username>, <password>) to login to the puck dns server"

class LoginFailed(Exception):
    def __init__(self, username):
        self.__username = username
    def __str__(self):
        return "Please check ur user credentials giving to user: {0}".format(self.__username)

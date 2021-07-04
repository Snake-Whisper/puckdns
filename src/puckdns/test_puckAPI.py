from socket import gethostbyname
from puckdnsExceptions import *
import puckdns
import os
import unittest

TESTDOMAINS = ["puckdns-py-api.ml", "puckdns2-py-api.ml", "puckdns3-py-api.ml"]


class A_TestPuckDnsApiLogin(unittest.TestCase):
    def setUp(self):
        self.puck = puckdns.API()

    def test_instance(self):
        self.assertTrue(isinstance(self.puck, puckdns.API))

    def test_a_tests_working(self):
        self.assertTrue("FOO".isupper())

    def test_env_username_set(self):
        self.assertTrue('PUCKDNS_USERNAME' in os.environ)

    def test_env_password_set(self):
        self.assertTrue('PUCKDNS_PASSWORD' in os.environ)

    def test_env_domain_set(self):
        self.assertTrue('PUCKDNS_DOMAIN' in os.environ)

    def test_not_logged_in_exception(self):
        self.assertRaises(NotLoggedIn, self.puck.getDomains)
        self.assertFalse(self.puck.isLoggedIn())

    def test_wrong_creds_exception(self):
        self.assertRaises(LoginFailed, self.puck.login,
                          os.environ['PUCKDNS_USERNAME'], "password")
        self.assertFalse(self.puck.isLoggedIn())

    def test_login_logout(self):
        self.assertIsNone(self.puck.login(
            os.environ['PUCKDNS_USERNAME'], os.environ['PUCKDNS_PASSWORD']))
        self.assertTrue(self.puck.isLoggedIn())
        self.puck.logout()
        self.test_not_logged_in_exception()


class B_PuckDnsApi(unittest.TestCase):
    HOST_IP = gethostbyname(os.environ['PUCKDNS_DOMAIN'])

    def setUp(self):
        self.puck = puckdns.API()
        self.puck.login(os.environ['PUCKDNS_USERNAME'],
                        os.environ['PUCKDNS_PASSWORD'])
        self.assertTrue(self.puck.isLoggedIn())

    def tearDown(self):
        self.puck.logout()
        self.assertFalse(self.puck.isLoggedIn())

    def test_a_tests_working(self):
        self.assertTrue("FOO".isupper())

    def test_get_domains(self):
        self.assertEqual(self.puck.getDomains(), [])

    def test_add_del_domain(self):
        self.assertEqual(self.puck.getDomains(), [])
        self.puck.addDomain(self.HOST_IP, "puckdns-py-api.ml")
        self.assertEqual(self.puck.getDomains(), ["puckdns-py-api.ml"])
        self.puck.delDomain("puckdns-py-api.ml")
        self.assertEqual(self.puck.getDomains(), [])

    def test_add_del_domains(self):
        self.assertEqual(self.puck.getDomains(), [])
        self.puck.addDomains(self.HOST_IP, TESTDOMAINS)
        self.assertEqual(self.puck.getDomains(), TESTDOMAINS)
        self.puck.delDomains(TESTDOMAINS)
        self.assertEqual(self.puck.getDomains(), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)

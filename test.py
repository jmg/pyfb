import unittest
from pyfb import Pyfb
from testdata import *

class pyfbTests(unittest.TestCase):

    def setUp(self):
        self.facebook = Pyfb(FACEBOOK_APP_ID)
        self.facebook.set_access_token(FACEBOOK_TOKEN)
        self.me = self.facebook.get_myself()

    def test_auth(self):
        self.assertEquals(type(self.me.name), type(unicode()))

    def test_get_friends(self):
        self.assertEquals(type(self.facebook.get_friends(self.me.id)), type(list()))

if __name__ == "__main__":

    unittest.main()


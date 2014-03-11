import unittest
import sys

try:
	import simplejson as json
except ImportError:
	import json

from pyfb import Pyfb

try:
    from .test_data import config
except ImportError:
	sys.stdout.write("\nERROR! You must have a test_data.py file providing the facebook app id and the access token.")
	sys.stdout.write("\n\nExample:")
	sys.stdout.write('\n\tconfig = {\n\t\t"FACEBOOK_APP_ID": "your_app_id"\n\t\t"FACEBOOK_TOKEN": "your_token"\n\t}\n')
	exit(1)


class PyfbTests(unittest.TestCase):

    pyfb_args = {}

    def setUp(self):
        self.pyfb = Pyfb(config["FACEBOOK_APP_ID"], **self.pyfb_args)
        self.pyfb.set_access_token(config["FACEBOOK_TOKEN"])
        self.me = self.pyfb.get_myself()

    def test_auth(self):
        self.assertEquals(type(self.me.name), type(str()))

    def test_get_friends(self):
        self.assertTrue(isinstance(self.pyfb.get_friends(self.me.id), list))

    def test_get_photos_paging(self):    	
        photos = self.pyfb.get_photos()
        more_photos = next(photos)
        more_more_photos = next(more_photos)

        if len(photos) < 25 and len(more_photos) > 0:
        	raise Exception()
        
        if len(photos) == 25 and len(more_photos) < 25 and len(more_more_photos) > 0:
        	raise Exception()

        self.assertTrue(isinstance(photos, list))
        self.assertTrue(isinstance(more_photos, list))
        self.assertTrue(isinstance(more_more_photos, list))

        self.assertEquals(len(photos), len(more_photos.previous()))
        self.assertEquals(photos.previous(), [])


class PyfbTestRawDataTests(PyfbTests):

    pyfb_args = {"raw_data": True }

    def test_auth(self):
        self.assertEquals(type(self.me["name"]), type(str()))

    def test_get_friends(self):
        friends = self.pyfb.get_friends(self.me["id"])
        self.assertTrue(isinstance(friends, list))
        for friend in friends:
            self.assertTrue(isinstance(friend, dict))

    def test_get_photos_paging(self):       
        """
            pagination is not supported by raw data since it returns a dictionary instead 
            of an object.
        """
        pass


from __future__ import print_function
import sys
import unittest

try:
	import simplejson as json
except ImportError:
	import json

from pyfb import Pyfb

#get a token from https://developers.facebook.com/tools/explorer/
config = {
    "FACEBOOK_APP_ID": "<YOUR_APP_ID>",
    "FACEBOOK_TOKEN": "<YOUR_ACCESS_TOKEN>",
}

class PyfbTests(unittest.TestCase):

    pyfb_args = {}

    def setUp(self):
        self.pyfb = Pyfb(config["FACEBOOK_APP_ID"], **self.pyfb_args)
        self.pyfb.set_access_token(config["FACEBOOK_TOKEN"])
        self.me = self.pyfb.get_myself()

    def test_auth(self):
        if sys.version_info > (3, 0):
            class_type = str
        else:
            class_type = unicode

        self.assertEquals(type(self.me.name), class_type)

    def test_get_friends(self):
        self.assertTrue(isinstance(self.pyfb.get_friends(self.me.id), list))

    def test_get_photos_paging(self):
        photos = self.pyfb.get_photos()
        more_photos = photos.next()
        more_more_photos = more_photos.next()

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
        if sys.version_info > (3, 0):
            class_type = str
        else:
            class_type = unicode

        self.assertEquals(type(self.me["name"]), class_type)

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


if __name__ == "__main__":

    unittest.main()


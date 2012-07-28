import unittest
try:
	import simplejson as json
except ImportError:
	import json

from pyfb import Pyfb

try:
	with open("test_data.json") as f:
		keys = json.loads(f.read())
except IOError:
	print "\nERROR! You must have a test_data.json file providing the facebook app id and the access token."
	print "\nExample:"
	print '\t{\n\t\t"FACEBOOK_APP_ID": "your_app_id"\n\t\t"FACEBOOK_TOKEN": "your_token"\n\t}\n'
	exit(1)


class pyfbTests(unittest.TestCase):

    def setUp(self):
        self.pyfb = Pyfb(keys["FACEBOOK_APP_ID"])
        self.pyfb.set_access_token(keys["FACEBOOK_TOKEN"])
        self.me = self.pyfb.get_myself()

    def test_auth(self):
        self.assertEquals(type(self.me.name), type(unicode()))

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


if __name__ == "__main__":

    unittest.main()


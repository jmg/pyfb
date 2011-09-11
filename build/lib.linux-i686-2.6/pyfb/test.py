from pyfb import Pyfb

FACEBOOK_APP_ID = '248639945152008'
FACEBOOK_SECRET_KEY = "dc9f36b43db5ef243f5ad30152bbe484"
FACEBOOK_REDIRECT_URL = 'http://www.gangaster.com/'

code = "NeFcDl-VwBbLaaPUZJed0uIybGU16qQFCPxUz2yZoAI.eyJpdiI6Ik5HMktDXzJ5ekxtTnpDWFpYc3JJQUEifQ.0_gdyHsesltXUxyOSStmwFj1m7MGm1-ZCkv2AQ5qhkgD_5Q1pjG9LCipfJBBhVqRVrSjCeJH4bf9cI3qGxGAC6rRbcQvwZCj8fEaHM7sbHxSJ-NWPqpIi1ay80XKlF_W"

facebook = Pyfb(FACEBOOK_APP_ID)

#facebook.get_authentication_code()

facebook = Pyfb(FACEBOOK_APP_ID)
facebook.get_access_token(FACEBOOK_SECRET_KEY, code, redirect_uri=FACEBOOK_REDIRECT_URL)
me = facebook.get_myself()

#u = facebook.get_user_by_id()
#facebook.publish("Python Rules!", 1438517184)

#st = facebook.get_statuses()[0]
#print st.message
#print facebook.like(st.id) 
#print facebook.get_auth_url

#print facebook.fql_query("SELECT name FROM user WHERE uid = 1438517184")



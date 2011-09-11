from pyfb import Pyfb

FACEBOOK_APP_ID = '178358228892649'
token = "178358228892649%7C0138d51ad50c294079008e48.1-1271577281%7C7CkyJwgeQucpXseZMDS7yf-UzMc"
secret = "cc2fbfac64784491fd84fc275b700496"

code = "R7tzsYDjPcdfKDJU0Z8Lw75uTZcOWefbUFN3NdmPNeM.eyJpdiI6InNTakZhV2xBZGRHWDNrdlY2STA1dmcifQ.ygqyI-sbb7WUjJSfYDDvSE-S7kcL47Rd3gFDjv_RfcE6uU9dRbcZsFsaw8YDNfJmwrxWPLaC1Awp_r6Sfun-KZm4xADlpsSmwjTOwg5Ie6whmQNxQhzvrtUVVjqzcqHy"

facebook = Pyfb(FACEBOOK_APP_ID)
#facebook.get_authentication_code()

token = facebook.get_access_token(secret, code)


#print facebook.authenticate()

u = facebook.delete("fds")
print u

#u = facebook.get_user_by_id()
#facebook.publish("Python Rules!", 1438517184)

#st = facebook.get_statuses()[0]
#print st.message
#print facebook.like(st.id) 
#print facebook.get_auth_url

#print facebook.fql_query("SELECT name FROM user WHERE uid = 1438517184")



from pyfb import Pyfb

#Your APP ID. You Need to register the application on facebook
#http://developers.facebook.com/
FACEBOOK_APP_ID = 'YOUR_APP_ID'

pyfb = Pyfb(FACEBOOK_APP_ID)

#Opens a new browser tab instance and authenticates with the facebook API
#It redirects to an url like http://www.facebook.com/connect/login_success.html#access_token=[access_token]&expires_in=0
pyfb.authenticate()

#Copy the [access_token] and enter it below
token = raw_input("Enter the access_token\n")

#Sets the authentication token
pyfb.set_access_token(token)

photos = pyfb.get_photos()

print "These are my photos:\n"
for photo in photos:
    print photo.picture

#Just call the method next to get the next page of photos!
more_photos = photos.next()

print "\nMore photos:\n"
for photo in more_photos:
    print photo.picture

more_more_photos = more_photos.next()

print "\nDo you want more?:\n"
for photo in more_more_photos:
    print photo.picture
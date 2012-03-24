# Pyfb - A Python Interface to the facebook Graph API

-------------------------------------------------------------------

### This is an Easy to Use Python Interface to the Facebook Graph API

It gives you methods to access your data on facebook and
provides objects instead of json dictionaries!

-------------------------------------------------------------------

Here's a little example to access your facebook profile data


```python

from pyfb import Pyfb

#Your APP ID. You Need to register the application on facebook
#http://developers.facebook.com/
FACEBOOK_APP_ID = 'YOUR_APP_ID'

facebook = Pyfb(FACEBOOK_APP_ID)

#Opens a new browser tab instance and authenticates with the facebook API
#It redirects to an url like http://www.facebook.com/connect/login_success.html#access_token=[access_token]&expires_in=0
facebook.authenticate()

#Copy the [access_token] and enter it below
token = raw_input("Enter the access_token\n")

#Sets the authentication token
facebook.set_access_token(token)

#Gets info about myself
me = facebook.get_myself()

print "-" * 40
print "Name: %s" % me.name
print "From: %s" % me.hometown.name
print

print "Speaks:"
for language in me.languages:
    print "- %s" % language.name

print
print "Worked at:"
for work in me.work:
    print "- %s" % work.employer.name

print "-" * 40

```

## Django Facebook Integration Using Pyfb

-----------------------------------------------------------------

It's easy to integrate pyfb with Django. Just see the following example:

### settings.py

```python

# Facebook related Settings
FACEBOOK_APP_ID = 'YOUR_APP_ID'
FACEBOOK_SECRET_KEY = 'YOUR_APP_SECRET_CODE'
FACEBOOK_REDIRECT_URL = 'http://www.YOUR_DOMAIN.com/facebook_login_success'

```

### views.py

```python

from pyfb import Pyfb
from django.http import HttpResponse, HttpResponseRedirect

from settings import FACEBOOK_APP_ID, FACEBOOK_SECRET_KEY, FACEBOOK_REDIRECT_URL

def index(request):
    return HttpResponse("""<button onclick="location.href='/facebook_login'">Facebook Login</button>""")

#This view redirects the user to facebook in order to get the code that allows
#pyfb to obtain the access_token in the facebook_login_success view
def facebook_login(request):

    facebook = Pyfb(FACEBOOK_APP_ID)
    return HttpResponseRedirect(facebook.get_auth_code_url(redirect_uri=FACEBOOK_REDIRECT_URL))

#This view must be refered in your FACEBOOK_REDIRECT_URL. For example: http://www.mywebsite.com/facebook_login_success/
def facebook_login_success(request):

    code = request.GET.get('code')

    facebook = Pyfb(FACEBOOK_APP_ID)
    facebook.get_access_token(FACEBOOK_SECRET_KEY, code, redirect_uri=FACEBOOK_REDIRECT_URL)
    me = facebook.get_myself()

    welcome = "Welcome <b>%s</b>. Your Facebook login has been completed successfully!"
    return HttpResponse(welcome % me.name)

```

### urls.py

```python

urlpatterns = patterns('',

    (r'^$', 'djangoapp.django_pyfb.views.index'),
    (r'^facebook_login/$', 'djangoapp.django_pyfb.views.facebook_login'),
    (r'^facebook_login_success/$', 'djangoapp.django_pyfb.views.facebook_login_success'),
)

```


## Integration with JS SDK

-----------------------------------------------------------------

You might user the JS SDK for login without a redirection to facebook (just open a popup) and Pyfb for backend api calls.

### index.html

```html

<html>
    <head>

    </head>
    <div id="fb-root"></div>
    <script>

        function isConnected(response) {
            return response.status == 'connected';
        }

        function getLoginStatus(FB) {

            FB.getLoginStatus(function(response) {

                if (isConnected(response)) {
                    onLogin(response);
                }
                else {
                    FB.login(onLogin);
                }
            });
        }

        function onLogin(response) {

            if (isConnected(response)) {
                location.href = '/facebook_javascript_login_sucess?access_token=' + response.authResponse.accessToken;
            }
        }

        window.fbAsyncInit = function() {

            FB.init({
                appId      : '{{FACEBOOK_APP_ID}}',
                channelUrl : 'http://localhost:8000/media/channel.html',
                status     : true,
                cookie     : true,
                xfbml      : true,
                oauth      : true,
            });

        };

        (function(d){
             var js, id = 'facebook-jssdk'; if (d.getElementById(id)) {return;}
             js = d.createElement('script'); js.id = id; js.async = true;
             js.src = "http://connect.facebook.net/en_US/all.js";
             d.getElementsByTagName('head')[0].appendChild(js);
        }(document));

    </script>

    <body>
        <button onclick="location.href='/facebook_login'">Facebook Python Login</button><br/><br/>
        <button onclick="getLoginStatus(FB)">Facebook Javascript Login</button>
    </body>
</html>

```

### views.py

```python

(...)
#Login with the js sdk and backend queries with pyfb
def facebook_javascript_login_sucess(request):

    access_token = request.GET.get("access_token")

    facebook = Pyfb(FACEBOOK_APP_ID)
    facebook.set_access_token(access_token)

    return _render_user(facebook)

(...)
```

### urls.py

```python

(...)
(r'^facebook_javascript_login_sucess/$', 'djangoapp.django_pyfb.views.facebook_javascript_login_sucess'),
(...)

```

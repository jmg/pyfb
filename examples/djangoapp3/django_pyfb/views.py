from pyfb import Pyfb
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from django.conf import settings

def index(request):
    return render_to_response("index.html", {"FACEBOOK_APP_ID": settings.FACEBOOK_APP_ID})


#This view redirects the user to facebook in order to get the code that allows
#pyfb to obtain the access_token in the facebook_login_success view
def facebook_login(request):

    facebook = Pyfb(settings.FACEBOOK_APP_ID)
    return HttpResponseRedirect(facebook.get_auth_code_url(redirect_uri=settings.FACEBOOK_REDIRECT_URL))


#This view must be refered in your FACEBOOK_REDIRECT_URL. For example: http://www.mywebsite.com/facebook_login_success/
def facebook_login_success(request):

    code = request.GET.get('code')

    facebook = Pyfb(settings.FACEBOOK_APP_ID)
    facebook.get_access_token(settings.FACEBOOK_SECRET_KEY, code, redirect_uri=settings.FACEBOOK_REDIRECT_URL)

    return _render_user(facebook)



#Login with the js sdk and backend queries with pyfb
def facebook_javascript_login_sucess(request):

    access_token = request.GET.get("access_token")

    facebook = Pyfb(settings.FACEBOOK_APP_ID)
    facebook.set_access_token(access_token)

    return _render_user(facebook)


def _render_user(facebook):

    me = facebook.get_myself()

    welcome = "Welcome <b>%s</b>. Your Facebook login has been completed successfully!"
    return HttpResponse(welcome % me.name)



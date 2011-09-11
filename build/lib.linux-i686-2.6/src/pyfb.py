"""
    $Id: pyfb.py

    This is an Easy to Use Python Interface to the Facebook Graph API

    It gives you methods to access your data on facebook and
    provides objects instead of json dictionaries!
"""

import urllib
import webbrowser

import auth
from utils import Json2ObjectsFactory

__author__ = "Juan Manuel Garcia"
__version__ = "0.2.2"

class Pyfb(object):
    """
        This class is Facade for FacebookClient
    """    
    
    def __init__(self, app_id, access_token=None, raw_data=False):
            
        self._client = FacebookClient(app_id, access_token, raw_data)   
    
    def authenticate(self):
        """
            Open your prefered web browser to make the authentication request
        """
        self._show_in_browser(self.get_auth_url())
        
    def get_authentication_code(self):
        """
            Open your prefered web browser to make the authentication request
        """
        self._show_in_browser(self.get_auth_code_url())
        
    def get_auth_url(self, redirect_uri=None):
        """
            Returns the authentication url
        """
        return self._client.get_auth_token_url(redirect_uri)
        
    def get_auth_code_url(self, redirect_uri=None):
        """
            Returns the url to get a authentication code
        """
        return self._client.get_auth_code_url(redirect_uri)
        
    def get_access_token(self, app_secret_key, secret_code, redirect_uri=None):
        """
            Gets the access token
        """
        return self._client.get_access_token(app_secret_key, secret_code, redirect_uri)
        
    def show_dialog(self, redirect_uri=None):
        """
            Open your prefered web browser to make the authentication request
        """
        self._show_in_browser(self.get_dialog_url(redirect_uri=redirect_uri))
        
    def get_dialog_url(self, redirect_uri=None):
        """
            Returns a url inside facebook that shows a dialog allowing 
            users to publish contents.
        """
        return self._client.get_dialog_url(redirect_uri)        
        
    def _show_in_browser(self, url):
        """
            Opens your prefered web browser to make the authentication request
        """
        webbrowser.open(url)
    
    def set_access_token(self, token):
        """
            Sets the access token. Necessary to make the requests that requires autenthication
        """
        self._client.access_token = token
    
    def set_permissions(self, permissions):
        """
            Sets a list of data access permissions that the user must give to the application
            e.g:
                permissions = [auth.USER_ABOUT_ME, auth.USER_LOCATION, auth.FRIENDS_PHOTOS, ...]
        """
        self._client.permissions = permissions
    
    def get_myself(self):
        """
            Gets myself data
        """
        return self._client.get_one("me", "FBUser")

    def get_user_by_id(self, id=None):
        """
            Gets an user by the id
        """
        if id is None:
            id = "me"
        return self._client.get_one(id, "FBUser")

    def get_friends(self, id=None):
        """
            Gets a list with your friends
        """
        return self._client.get_list(id, "Friends")

    def get_statuses(self, id=None):
        """
            Gets a list of status objects
        """
        return self._client.get_list(id, "Statuses")

    def get_photos(self, id=None):
        """
            Gets a list of photos objects
        """
        return self._client.get_list(id, "Photos")
        
    def get_comments(self, id=None):
        """
            Gets a list of photos objects
        """
        return self._client.get_list(id, "Comments")

    def publish(self, message, id=None):
        """
            Publishes a message on the wall
        """
        self._client.push(id, "feed", message=message)
        
    def comment(self, message, id=None):
        """
            Publishes a message on the wall
        """
        self._client.push(id, "comments", message=message)
        
    def get_likes(self, id=None):
        """
            Get a list of liked objects
        """
        return self._client.get_list(id, "likes")
        
    def like(self, id):
        """
            LIKE: It Doesn't work. Seems to be a bug on the Graph API 
            http://bugs.developers.facebook.net/show_bug.cgi?id=10714
        """
        print self.like.__doc__
        return self._client.push(id, "likes")
        
    def delete(self, id):
        """ 
            Deletes a object
        """
        self._client.delete(id)
        
    def fql_query(self, query):
        """
            Executes a FBQL query
        """
        return self._client.execute_fql_query(query)


class FacebookClient(object):
    """
        This class implements the interface to the Facebook Graph API
    """
    
    FACEBOOK_URL = "https://www.facebook.com/"
    GRAPH_URL = "https://graph.facebook.com/"
    API_URL = "https://api.facebook.com/"
    
    BASE_AUTH_URL = "%soauth/authorize?" % GRAPH_URL
    DIALOG_BASE_URL = "%sdialog/feed?" % FACEBOOK_URL
    FBQL_BASE_URL = "%smethod/fql.query?" % API_URL
    BASE_TOKEN_URL = "%soauth/access_token?" % GRAPH_URL
    
    DEFAULT_REDIRECT_URI = "http://www.facebook.com/connect/login_success.html"
    DEFAULT_SCOPE = auth.ALL_PERMISSIONS
    DEFAULT_DIALOG_URI = "http://www.example.com/response/"
 
     #A factory to make objects from a json
    factory = Json2ObjectsFactory()       

    def __init__(self, app_id, access_token=None, raw_data=None):

        self.app_id = app_id
        self.access_token = access_token    
        self.raw_data = raw_data
        self.permissions = self.DEFAULT_SCOPE
        
    def _make_request(self, url, **data):
        """
            Makes a simple request. If not data is a GET else is a POST.
        """
        if not data:
            data = None
        return urllib.urlopen(url, data).read()
    
    def _make_auth_request(self, path, **data):
        """
            Makes a request to the facebook Graph API.
            This method requires authentication!
            Don't forgot to get the access token before use it.
        """
        if self.access_token is None:
            raise PyfbException("Must Be authenticated. Do you forgot to get the access token?")

        token_url = "?access_token=%s" % self.access_token
        url = "%s%s%s" % (self.GRAPH_URL, path, token_url)
        if data:
            post_data = urllib.urlencode(data)
        else:
            post_data = None
        return urllib.urlopen(url, post_data).read()

    def _make_object(self, name, data):
        """
            Uses the factory to make an object from a json
        """
        if not self.raw_data:
            return self.factory.make_object(name, data)
        return self.factory.loads(data)
    
    def _get_url_path(self, dic):
    
        return urllib.urlencode(dic)
    
    def _get_auth_url(self, params, redirect_uri):
        """
            Returns the authentication url
        """
        if redirect_uri is None:
            redirect_uri = self.DEFAULT_REDIRECT_URI
        params['redirect_uri'] = redirect_uri
        
        url_path = self._get_url_path(params)
        url = "%s%s" % (self.BASE_AUTH_URL, url_path)
        return url
        
    def _get_permissions(self):
        
        return ",".join(self.permissions)        
    
    def get_auth_token_url(self, redirect_uri):
        """
            Returns the authentication token url
        """          
        print self._get_permissions()          
        params = {
            "client_id": self.app_id,
            "type": "user_agent",
            "scope": self._get_permissions(),
        }
        return self._get_auth_url(params, redirect_uri)
        
    def get_auth_code_url(self, redirect_uri):
        """
            Returns the url to get a authentication code
        """
        params = {
            "client_id": self.app_id,
            "scope": self._get_permissions(),
        }
        return self._get_auth_url(params, redirect_uri)
        
    def get_access_token(self, app_secret_key, secret_code, redirect_uri):
        
        if redirect_uri is None:
            redirect_uri = self.DEFAULT_REDIRECT_URI
        
        self.secret_key = app_secret_key
        
        url_path = self._get_url_path({
            "client_id": self.app_id,
            "client_secret" : app_secret_key,
            "redirect_uri" : redirect_uri,
            "code" : secret_code,
        })
        url = "%s%s" % (self.BASE_TOKEN_URL, url_path)
        
        data = self._make_request(url)
        
        if not "access_token" in data:
            ex = self.factory.make_object('Error', data)
            raise PyfbException(ex.error.message)
        
        token = data.split("=")[1]
        
        self.access_token = token
        return token        
        
    def get_dialog_url(self, redirect_uri):
        
        if redirect_uri is None:
            redirect_uri = self.DEFAULT_DIALOG_URI
            
        url_path = self._get_url_path({
            "app_id" : self.app_id,
            "redirect_uri": redirect_uri,
        })
        url = "%s%s" % (self.DIALOG_BASE_URL, url_path)
        return url

    def get_one(self, path, object_name):
        """
            Gets one object
        """
        data = self._make_auth_request(path)
        obj = self._make_object(object_name, data)
        
        if hasattr(obj, 'error'):
            raise PyfbException(obj.error.message)
            
        return obj

    def get_list(self, id, path, object_name=None):
        """
            Gets A list of objects
        """
        if id is None:
            id = "me"
        if object_name is None:
            object_name = path
        path = "%s/%s" % (id, path.lower())
        return self.get_one(path, object_name).__dict__[object_name]
        
    def push(self, id, path, **data):
        """
            Pushes data to facebook
        """
        if id is None:
            id = "me"
        path = "%s/%s" % (id, path)
        self._make_auth_request(path, **data)
        
    def delete(self, id):
        """
            Deletes a object by id
        """
        data = {"method": "delete"}
        self._make_auth_request(id, **data)
        
    def _get_table_name(self, query):
        """
            Try to get the table name from a fql query
        """
        KEY = "FROM"
        try:
            index = query.index(KEY) + len(KEY) + 1
            table = query[index:].strip().split(" ")[0]
            return table
        except Exception, e:
            raise PyfbException("Invalid FQL Sintax")
    
    def execute_fql_query(self, query):
        """
            Executes a FBQL query and return a list of objects
        """
        table = self._get_table_name(query)
        url_path = self._get_url_path({'query' : query, 'format' : 'json'})
        url = "%s%s" % (self.FBQL_BASE_URL, url_path)
        data = self._make_request(url)
        return self.factory.make_objects_list(table, data)
    

class PyfbException(Exception):
    """
        A PyFB Exception class
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


"""
    This is an Easy to Use Python Interface to the Facebook Graph API

    It gives you methods to access your data on facebook and
    provides objects instead of json dictionaries!
"""

import webbrowser
from client import FacebookClient, PyfbException
import json

class Pyfb(object):
    """
        This class is Facade for FacebookClient
    """

    def __init__(self, app_id, access_token=None, raw_data=False, permissions=None):

        self._client = FacebookClient(app_id, access_token=access_token, raw_data=raw_data, permissions=permissions)

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

    def get_auth_code_url(self, redirect_uri=None, state=None):
        """
            Returns the url to get a authentication code
        """
        return self._client.get_auth_code_url(redirect_uri, state=state)

    def get_access_token(self, app_secret_key, secret_code, redirect_uri=None):
        """
            Gets the access token
        """
        return self._client.get_access_token(app_secret_key, secret_code, redirect_uri)

    def exchange_token(self, app_secret_key, exchange_token):
        """
             Exchanges a short-lived access token (like those obtained from client-side JS api)
             for a longer-lived access token
        """
        return self._client.exchange_token(app_secret_key, exchange_token)

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

    def get_myself(self, extra_params=None):
        """
            Gets myself data
        """
        return self._client.get_one("me", "FBUser", extra_params=extra_params)

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

    def publish(self, message, id=None, **kwargs):
        """
            Publishes a message on the wall
        """
        return self._client.push(id, "feed", message=message, **kwargs)

    def publish_picture(self,message,id=None,**kwargs):
        """
            Publish picture
        """
        return self._client.push(id,"photos",message=message,**kwargs);

    def comment(self, message, id=None, **kwargs):
        """
            Publishes a message on the wall
        """
        return self._client.push(id, "comments", message=message, **kwargs)

    def get_likes(self, id=None):
        """
            Get a list of liked objects
        """
        return self._client.get_list(id, "likes")

    def get_pages(self, id=None):
        """
            Get a list of Facebook Pages user has access to
        """
        return self._client.get_list(id, 'accounts', 'FBPage')

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
        return self._client.delete(id)

    def fql_query(self, query):
        """
            Executes a FBQL query
        """
        return self._client.execute_fql_query(query)

    def request(self, path, **data):
        """
            Executes a request to the api
        """
        response = self._client._make_auth_request(path, **data)
        return json.loads(response)

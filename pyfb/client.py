"""
    The implementation of the Facebook Client
"""

from urlparse import parse_qsl
from utils import Json2ObjectsFactory
import auth
import requests
import urllib
import urllib2

class FacebookClient(object):
    """
        This class implements the interface to the Facebook Graph API
    """

    FACEBOOK_DOMAIN = "www.facebook.com"
    GRAPH_DOMAIN = "graph.facebook.com"
    API_DOMAIN = "api.facebook.com"

    DEFAULT_REDIRECT_URI = "http://www.facebook.com/connect/login_success.html"
    DEFAULT_SCOPE = auth.ALL_PERMISSIONS
    DEFAULT_DIALOG_URI = "http://www.example.com/response/"

     #A factory to make objects from a json
    factory = Json2ObjectsFactory()

    def __init__(self, app_id, access_token=None):
        self.app_id = app_id
        self.access_token = access_token
        self.permissions = self.DEFAULT_SCOPE
        self.expires = None

        self.session = requests.Session()

    def _make_request(self, method="get", domain=GRAPH_DOMAIN, path=None, params=None, auth=True, **data):
        """
            Makes a request to the facebook Graph API.
            This method requires authentication!
            Don't forgot to get the access token before use it.
        """
        if params is None:
            params = {}
        else:
            for key, value in params.items():
                if value is None:
                    del params[key]

        if auth:
            if self.access_token is None:
                raise PyfbException("Must Be authenticated. Do you forgot to get the access token?")

            params["access_token"] = self.access_token

        url = "https://%s/%s" % (domain, path)

        response = self.session.request(method, url, params, data)
        if response.status_code < 200 or response.status_code > 299:
            raise PyfbException("Got response %s" % response.status_code)

        return response.content

    def _build_url(self, domain, path, params):
        return "https://%s/%s?%s" % (domain, path, urllib.urlencode(params))

    def _get_auth_url(self, params, redirect_uri):
        """
            Returns the authentication url
        """
        params['redirect_uri'] = redirect_uri

        return self._build_url(self.FACEBOOK_DOMAIN, "oauth/authorize", params)

    def _get_permissions(self):
        return ",".join(self.permissions)

    def get_auth_token_url(self, redirect_uri=DEFAULT_REDIRECT_URI):
        """
            Returns the authentication token url
        """
        params = {
            "client_id": self.app_id,
            "type": "user_agent",
            "scope": self._get_permissions(),
        }

        return self._get_auth_url(params, redirect_uri)

    def get_auth_code_url(self, redirect_uri=DEFAULT_REDIRECT_URI):
        """
            Returns the url to get a authentication code
        """
        params = {
            "client_id": self.app_id,
            "scope": self._get_permissions(),
        }

        return self._get_auth_url(params, redirect_uri)

    def get_access_token(self, app_secret_key, secret_code, redirect_uri=DEFAULT_REDIRECT_URI):
        params = {
            "client_id": self.app_id,
            "client_secret" : app_secret_key,
            "redirect_uri" : redirect_uri,
            "code" : secret_code,
        }

        data = self._make_request(path="oauth/access_token", params=params, auth=False)

        data = dict(parse_qsl(data))

        self.access_token = data.get('access_token')
        self.expires = data.get('expires')

        return self.access_token

    def get_dialog_url(self, redirect_uri=DEFAULT_DIALOG_URI):
        params = {
            "app_id" : self.app_id,
            "redirect_uri": redirect_uri,
        }

        return self._build_url(self.FACEBOOK_DOMAIN, "dialog/feed", params)

    def get_one(self, path, object_name, **params):
        """
            Gets one object
        """
        data = self._make_request(path=path, params=params)

        return self.factory.make_object(object_name, data)

    def get_list(self, id, path, object_name=None, **params):
        """
            Gets A list of objects
        """
        if id is None:
            id = "me"
        if object_name is None:
            object_name = path
        path = "%s/%s" % (id, path.lower())

        return self.get_one(path, object_name, **params).data

    def push(self, id, path, **data):
        """
            Pushes data to facebook
        """
        if id is None:
            id = "me"
        path = "%s/%s" % (id, path)

        self._make_request(method="put", path=path, **data)

    def delete(self, id):
        """
            Deletes a object by id
        """
        data = {"method": "delete"}

        self._make_request(method="delete", path=id, **data)

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
        params = {'query' : query, 'format' : 'json'}
        data = self._make_request(domain=self.API_DOMAIN, path="method/fql.query", params=params)
        return self.factory.make_objects_list(table, data)

class PyfbException(Exception):
    pass

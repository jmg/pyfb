"""
    $Id: utils.py

    This file provides utilities to the pyfb library
"""

import simplejson

class NamedObject(object):
    """
        Builds an object of a runtime generated class with a name
        passed by argument.
    """
    def __new__(cls, name):
        return type(str(name), (object,), {})


class Json2ObjectsFactory(object):
    """
        Converts a json-like dictionary into an object.

        It navigates recursively into the dictionary turning
        everything into an object.
    """

    def _make_objects_list(self, name, values):
        return [self._make_object(name, value) for value in values]

    def _make_object_dict(self, name, dic):
        #Life's easy. For Python Programmers BTW ;-).
        obj = NamedObject(name)
        for key, value in dic.iteritems():
            setattr(obj, key, self._make_object(name, obj))
        return obj

    def make_object(self, name, obj):
        obj = simplejson.loads(obj)

        if isinstance(obj, dict):
            return self._make_object_dict(name, obj)
        elif isinstance(obj, list):
            return self._make_objects_list(name, obj)
        else:
            return obj

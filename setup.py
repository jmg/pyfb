#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pyfb import __author__, __version__, __license__

setup(
    name='pyfb',
    version=__version__,
    description='A Python Interface to the Facebook Graph API',
    author=__author__,
    author_email = "jmg.utn@gmail.com",
    license = __license__,
    keywords = "Facebook Graph API Wrapper Python",
    url='http://code.google.com/p/pyfb/',
    packages=['pyfb'],
    install_requires=[
        'simplejson',
    ],
)

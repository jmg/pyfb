#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from src import pyfb

setup(
    name='pyfb',
    version=pyfb.__version__,
    description='A Python Interface to the Facebook Graph API',
    author='Juan Manuel García',
    author_email = "jmg.utn@gmail.com",
    license = "GPL v3",
    keywords = "Facebook Graph API Wrapper Python",
    url='http://code.google.com/p/pyfb/',    
    packages = find_packages(),    
    install_requires=[
        'simplejson',
    ],
)

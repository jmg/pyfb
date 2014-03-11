#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='pyfb',
    version="0.4.2",
    description='A Python Interface to the Facebook Graph API',
    author="Juan Manuel Garcia",
    author_email = "jmg.utn@gmail.com",
    license = "GPL v3",
    keywords = "Facebook Graph API Wrapper Python",
    url='http://code.google.com/p/pyfb/',
    packages=['pyfb'],
    install_requires=[
        'simplejson',
    ],
)

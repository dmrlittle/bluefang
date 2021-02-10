#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:12:38 2020

@author: mrlittle
"""


import requests
import pickle

url = 'http://localhost:5000/afre/create'
url_1 = 'http://localhost:5000/afre/drop'
url1 = 'http://localhost:5000/afre/add/3'
url2 = 'http://localhost:5000/afre/push/3'
url3 = 'http://localhost:5000/afre/pull/3'
myobj = 2

x = requests.get(url)

#y = pickle.loads(x.content)x
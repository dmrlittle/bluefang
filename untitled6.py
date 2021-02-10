#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 14:11:36 2020

@author: mrlittle
"""


from flask import Flask, request, Response
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return Response(status=400)


@app.route("/about")
def about():
    return "<h1>About Page</h1>"


if __name__ == '__main__':
    app.run(debug=True)
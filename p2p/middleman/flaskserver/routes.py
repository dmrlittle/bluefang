# -*- coding: utf-8 -*-
from flask import request, Response
from flaskserver import app, db
from flaskserver.models import Downloads, Peers
import pickle, secrets, json


def tokgen():
    codes = [download.code for download in Downloads.query.all()]
    while True:
        tok = secrets.token_hex(6)
        if(tok not in codes):
            break
    return tok

@app.route("/create",methods=['post'])
def create():
    if request.method != 'POST':
        return Response(status=400)
    data = pickle.loads(request.get_data())
    tok = tokgen()
    download = Downloads(code = tok, url = data[0])
    db.session.add(download)
    db.session.commit()
    return Response(response = pickle.dumps(tok), status = 200)

@app.route("/join/<string:code>")
def join(code):
    codes = [download.code for download in Downloads.query.all()]
    if code in codes:
        return Response(response = pickle.dumps(code), status = 200)
    return Response(status=400)

@app.route("/fetch/<string:code>")
def fetch(code):
    download = Downloads.query.filter_by(code = code).first()
    if(not download):
        return Response(status=400)
    peers = [[peer.ipv6,json.loads(peer.r)] for peer in download.peers]
    return Response(response = pickle.dumps(peers), status = 200)

@app.route("/add/<string:code>",methods = ['post'])
def add(code):
    download = Downloads.query.filter_by(code=code).first()
    if(not download):
        return Response(status=400)
    ipv6, r = pickle.loads(request.get_data())
    peer = Peers(r = json.dumps(r), ipv6 = ipv6,
                 download_id=download.id)
    db.session.add(peer)
    db.session.commit()
    return Response(status=200)

@app.route("/modify/<string:code>",methods = ['post'])
def modify(code):
    download = Downloads.query.filter_by(code=code).first()
    if(not download):
        return Response(status=400)
    rstart, rend, rnewend = pickle.loads(request.get_data())
    for peer in download.peers:
        if peer.r == json.dumps([rstart, rend]):
            peer.r = json.dumps([rstart, rnewend])
    db.session.commit()
    return Response(status=200)

@app.route("/delete/<string:code>", methods = ['post'])
def delete(code):
    download = Downloads.query.filter_by(code=code).first()
    if(not download):
        return Response(status=400)
    r = pickle.loads(request.get_data())
    for peer in download.peers:
        if peer.r == json.dumps(r):
            break
    else:
        return Response(status=400)
    db.session.delete(peer)
    db.session.commit()
    return Response(status=200)

@app.route("/drop/<string:code>")
def drop(code):
    download = Downloads.query.filter_by(code=code).first()
    if(not download):
        return Response(status=400)
    for peer in download.peers:
        db.session.delete(peer)
    db.session.delete(download)
    db.session.commit()
    return Response(status=200)
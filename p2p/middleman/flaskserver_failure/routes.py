# -*- coding: utf-8 -*-
from flask import request
from flaskserver import app, db
from flaskserver.models import Downloads, Peers
import pickle


@app.route("/<string:code>/create")
def create(code):
    download = Downloads(code=code)
    db.session.add(download)
    db.session.commit()
    return '0'

@app.route("/fetch")
def fetch():
    downloads = Downloads.query.all()
    temp1=[download.code for download in downloads]
    return pickle.dumps(temp1)

@app.route("/<string:code>/add/<int:name>",methods=['post'])
def add(code,name):
    temp1 = Downloads.query.filter_by(code=code).first()
    if(not temp1):
        return '1'
    temp2 = pickle.loads(request.get_data())
    peer = Peers(name=name, rstart=temp2[0], rmid=temp2[1],
                 rend=temp2[2], rsize=temp2[2]-temp2[0]+1,
                 download_id=temp1.id)
    db.session.add(peer)
    db.session.commit()
    return '0'

@app.route("/<string:code>/push/<int:name>",methods=['post'])
def push(code,name):
    download = Downloads.query.filter_by(code=code).first()
    if(not download):
        return '1'
    for peer in download.peers:
        if peer.name == name:
            break
    else:
        return '2'
    temp1= request.get_data()
    peer.rmid = pickle.loads(temp1)
    db.session.commit()
    return '0'

@app.route("/<string:code>/pull/<int:name>")
def pull(code,name):
    download = Downloads.query.filter_by(code=code).first()
    if(not download):
        return '1'
    for peer in download.peers:
        if peer.name == name:
            break
    else:
        return '2'
    temp1=peer.rend
    return pickle.dumps(temp1)

@app.route("/<string:code>/delete/<int:name>")
def delete(code,name):
    download = Downloads.query.filter_by(code=code).first()
    if(not download):
        return '1'
    for peer in download.peers:
        if peer.name == name:
            break
    else:
        return '2'
    db.session.delete(peer)
    db.session.commit()
    return '0'

@app.route("/<string:code>/drop")
def drop(code):
    download = Downloads.query.filter_by(code=code).first()
    if(not download):
        return '1'
    for peer in download.peers:
        db.session.delete(peer)
    db.session.delete(download)
    db.session.commit()
    return '0'



    


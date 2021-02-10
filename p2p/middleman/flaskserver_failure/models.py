# -*- coding: utf-8 -*-
from flaskserver import db

class Downloads(db.Model):
    __tablename__ = 'downloads'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    peers=db.relationship('Peers',backref='download')
    
    def __repr__(self):
        return f"Download('{self.code}')"
    
class Peers(db.Model):
    __tablename__ = 'peers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    rstart = db.Column(db.Integer, nullable=False, default=0)
    rmid = db.Column(db.Integer, nullable=False)
    rend = db.Column(db.Integer, nullable=False)
    rsize = db.Column(db.Integer, nullable=False)
    download_id=db.Column(db.Integer,db.ForeignKey('downloads.id'),nullable=False)

    def __repr__(self):
        return f"Peer('{self.name}')"
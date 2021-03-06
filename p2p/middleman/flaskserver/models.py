# -*- coding: utf-8 -*-
from flaskserver import db

class Downloads(db.Model):
    __tablename__ = 'downloads'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    url = db.Column(db.String(), nullable=False)
    peers = db.relationship('Peers',backref='download')
    
    def __repr__(self):
        return f"Download('{self.code}')"
    
class Peers(db.Model):
    __tablename__ = 'peers'
    id = db.Column(db.Integer, primary_key=True)
    r = db.Column(db.String(), nullable=False)
    ipv6 = db.Column(db.String(50), nullable=False)
    download_id = db.Column(db.Integer,db.ForeignKey('downloads.id'),nullable=False)

    def __repr__(self):
        return f"Peer('{self.r}')"
    

from app import db
import datetime

class Images(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    type = db.Column(db.String(255))
    event_id = db.Column(db.Integer,db.ForeignKey('events.event_id'))
    date_added = db.Column(db.DateTime,default=datetime.datetime.now())
    date_updated = db.Column(db.DateTime,default=datetime.datetime.now())
    category = db.Column(db.String(255))
    video_id = db.Column(db.Integer)
    position = db.Column(db.Integer, unique=True)

    def __init__(self, name,type,event_id=None):
        self.name = name
        self.type = type
        self.event_id = event_id


    def __repr__(self):
        return '<Image %r>' % (self.name)



class Events(db.Model):
    __tablename__ = "events"

    event_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, event_id):
        self.event_id = event_id

    def __repr__(self):
        return '<Image %r>' % (self.name)
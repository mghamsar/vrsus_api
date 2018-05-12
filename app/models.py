from app import db
import datetime


class ImagesData(db.Model):

    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    image_name = db.Column('name', db.String(255), index=True, unique=True)
    type = db.Column(db.String(255))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    event_name = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.datetime.now())
    date_updated = db.Column(db.DateTime, default=datetime.datetime.now())
    category = db.Column(db.String(255))
    video_id = db.Column('video_id', db.Integer)
    position = db.Column(db.Integer, unique=True)

    def __init__(
            self,
            image_name,
            type=None, event_id=None,
            event_name=None,
            date_added=None,
            date_updated=None,
            category=None,
            video_id=None,
            position=None):
        self.image_name = image_name
        self.type = type if type is not None else None
        self.event_id = event_id if event_id is not None else None
        self.event_name = event_name if event_name is not None else None
        self.date_added = date_added if date_added is not None else None
        self.date_updated = date_updated if date_updated is not None else None
        self.category = category if category is not None else None
        self.video_id = video_id if video_id is not None else None
        self.position = position if position is not None else None

    # def __repr__(self):
    # 	results = {}
    # 	results['imagename'] = self.name
    # 	results['type'] = self.type
    #   return self.name


class EventsData(db.Model):
    __tablename__ = "events"

    event_id = db.Column(db.Integer, primary_key=True, unique=True)
    event_name = db.Column(db.String(255), index=True, unique=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    venue_id = db.Column(db.Integer)
    venue_name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.datetime.now())
    date_updated = db.Column(db.DateTime, default=datetime.datetime.now())
    category = db.Column(db.String(255))

    def __init__(self,
                 event_name,
                 date=None,
                 venue_id=None,
                 venue_name=None,
                 type=None,
                 date_added=None,
                 date_updated=None,
                 category=None):
        self.event_name = event_name
        self.date = date if date is not None else None
        self.venue_id = venue_id if venue_id is not None else None
        self.venue_name = venue_name if venue_name is not None else None
        self.type = type if type is not None else None
        self.date_added = date_added if date_added is not None else None
        self.date_updated = date_updated if date_updated is not None else None
        self.category = category if category is not None else None

    # def __repr__(self):
    #     return self.event_id


class VideosData(db.Model):
    __tablename__ = "videos"

    video_id = db.Column('id', db.Integer, primary_key=True, unique=True)
    video_name = db.Column('name', db.String(255), index=True, unique=True)
    event_id = db.Column(db.Integer, unique=True)
    event_name = db.Column(db.String(255))
    date_added = db.Column(db.DateTime, default=datetime.datetime.now())
    date_updated = db.Column(db.DateTime, default=datetime.datetime.now())
    category = db.Column(db.String(255))
    type = db.Column(db.String(255))

    def __init__(
            self,
            name,
            event_id=None,
            event_name=None,
            date_added=None,
            date_updated=None,
            category=None,
            type=None):
        self.video_name = name
        self.event_id = event_id if event_id is not None else None
        self.event_name = event_name if event_name is not None else None
        self.date_added = date_added if date_added is not None else None
        self.date_updated = date_updated if date_updated is not None else None
        self.category = category if category is not None else None
        self.type = type if type is not None else None

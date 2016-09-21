from app import models,db
from flask import request, jsonify, redirect, url_for

import boto, boto.s3.connection
import config
import time

class Events:

    def getEvents(self):
        name = request.args.get('name') if request.args.get('name') is not None else None
        category = request.args.get('category') if request.args.get('category') is not None else None
        count = request.args.get('count') if request.args.get('count') is not None else None
        eventType = request.args.get('type') if request.args.get('type') is not None else None
        venue = request.args.get('venue') if request.args.get('venue') is not None else None

        events = models.EventsData.query.all()
        if name is not None and category is not None:
            events = models.EventsData.query.filter_by(event_name=name,category=category).all()
        elif name is not None: 
            events = models.EventsData.query.filter_by(event_name=name).all()
        elif category is not None: 
            events = models.EventsData.query.filter_by(category=category).all()
        elif eventType is not None: 
            events = models.EventsData.query.filter_by(type=eventType).all()


        if count is not None:
            events = events.limit(int(count)).all()

        results = {}
        if events:
            for row, values in enumerate(events):
                results[row] = {
                    'id':values.event_id,
                    'name':values.event_name,
                    'date':values.date,
                    'venue':values.venue_name,
                    'type':values.type,
                    #'imagefilename':values[10],
                    #'videofilename':values[9]
                    }

        if category == 'hackneywicked':
            return self.orderEvents(results)

        else:
            return jsonify(results)


    def orderEvents(self,events):

        results = {}

        # 1 live_painting
        # 2 wallis_road_03
        # 3 mother_studios_01
        # 4 mother_studios_03
        # 5 illustration_design
        # 6 photo_studio
        # 7 mother_studio_02
        # 8 micks_garage
        # 9 parking_lot_01

        for i in range(len(events)):
            video = events[i]["videofilename"]

            if video == "live_painting.mp4":
                results[0]=events[i]
            if video == "wallis_road_03.mp4":
                results[1]=events[i]
            if video == "mother_studios_01.mp4":
                results[2]=events[i]
            if video == "mother_studios_03.mp4":
                results[3]=events[i]
            if video == "illustration_design.mp4":
                results[4]=events[i]
            if video == "photo_studio.mp4":
                results[5]=events[i]
            if video == "mother_studio_02.mp4":
                results[6]=events[i]
            if video == "micks_garage.mp4":
                results[7]=events[i]
            if video == "parking_lot_01.mp4":
                results[8]=events[i]

        return jsonify(results)


    def updateEvent(self, eventname, eventtype=None, eventcategory=None):

        now = time.strftime('%Y-%m-%d')
        ev = models.EventsData.query.filter_by(event_name=eventname).first()

        if ev is not None:
            if eventtype is not None:
                ev.type = eventtype
            if eventcategory is not None: 
                ev.category = eventcategory
        else: 
            ev = models.EventsData(eventname, date_added=now, date_updated=now)
            if eventtype is not None:
                ev.type = eventtype
            if eventcategory is not None: 
                ev.category = eventcategory

        db.session.add(img)
        db.session.commit()
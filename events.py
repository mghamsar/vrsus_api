import MySQLdb
import boto, boto.s3.connection
import os, time, json
from flask import jsonify, request, Response
from config import Config
import config
from db import Db

class Events:
    def __init__(self):
        return None


    def getEvents(self):
        name = request.args.get('name') if request.args.get('name') is not None else None
        category = request.args.get('category') if request.args.get('category') is not None else None
        count = request.args.get('count') if request.args.get('count') is not None else None
        eventType = request.args.get('type') if request.args.get('type') is not None else None
        venue = request.args.get('venue') if request.args.get('venue') is not None else None

        query = "SELECT e.*, v.name, i.name from events as e \
        LEFT JOIN videos as v on e.event_id=v.event_id \
        LEFT JOIN images as i on v.id=i.video_id"

        if name is not None and category is not None:
            query = query + " where e.event_name='"+name+"' AND e.category='"+category+"'"
        elif eventType is not None: 
            query = query + " where e.type='"+eventType+"'"
        elif category is not None:
            query = query + " where e.category='"+category+"'"
        elif name is not None:
            query = query + " where e.event_name='"+name+"'"
        elif venue is not None: 
            query = query + " WHERE e.venue_name='"+venue+"'"
        
        if count is not None:
             query = query + " LIMIT "+str(count)

        query = query +";"

        dbi = Db()
        data = dbi.getQuery(query)
        con = Config()

        results = {}
        if data is not None and len(data) >= 1:
            for row, values in enumerate(data):
                results[row] = {
                    'id':values[0],
                    'name':values[1],
                    'date':con.date_handler(values[2]),
                    'venue':values[4],
                    'type':values[5],
                    'imagefilename':values[10],
                    'videofilename':values[9]
                    }

        print category
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

        #print results
        return jsonify(results)

    def updateEvent(self, eventname, eventtype=None, eventcategory=None):

        now = time.strftime('%Y-%m-%d')
        query = "SELECT event_id,event_name from events where event_name='"+eventname+"';"
        dbi = Db();
        data = dbi.getQuery(query);

        if data:
            id, name = data[0]
            print id, name

            if eventtype is not None and eventcategory is not None:
                addeventquery = "UPDATE events SET type='"+eventtype+"', category='"+eventcategory+"' WHERE event_id="+str(id)+";"
                dbi.addQuery(addeventquery);

            elif eventtype is not None:
                addeventquery = "UPDATE events SET type='"+eventtype+"' WHERE event_id="+str(id)+";"
                dbi.addQuery(addeventquery);

        else:
            if eventtype is not None and eventcategory is not None:
                addeventquery = "INSERT INTO events (event_name,type,category,date_added,date_updated)\
                VALUES ('"+eventname+"','"+eventtype+"','"+eventcategory+"','"+now+"','"+now+"');"
                id2 = dbi.addQuery(addeventquery);

            elif eventtype is not None:
                addeventquery = "INSERT INTO events (event_name,type,date_added,date_updated) VALUES ('"+eventname+"','"+eventtype+"','"+now+"','"+now+"');"
                id2 = dbi.addQuery(addeventquery);

            query = "SELECT event_id,event_name from events where event_id="+str(id2)+";"
            data = dbi.getQuery(query);

        return data
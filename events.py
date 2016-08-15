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

        query = "SELECT e.*, v.name, i.name from events as e \
        LEFT JOIN videos as v on e.event_id=v.event_id \
        LEFT JOIN images as i on e.event_id=i.event_id"

        if name is not None and category is not None:
            query = query + " where e.event_name='"+name+"' AND e.category='"+category+"'"
        elif eventType is not None: 
            query = query + " where e.type='"+eventType+"'"
        elif category is not None:
            query = query + " where e.category='"+category+"'"
        elif name is not None:
            query = query + " where e.event_name='"+name+"'"
        
        if count is not None:
             query = query + " LIMIT "+str(count)

        query = query +";"

        dbi = Db()
        data = dbi.getQuery(query)
        con = Config()

        results = {}
        if data is not None and len(data) >= 1:
            for row, values in enumerate(data):
                print(str(values))
                results[row] = {
                    'id':values[0],
                    'name':values[1],
                    'date':con.date_handler(values[2]),
                    'venue':values[4],
                    'type':values[5],
                    'imagefilename':values[10],
                    'videofilename':values[9]
                    }

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
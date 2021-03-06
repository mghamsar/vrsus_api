import MySQLdb
import boto, boto.s3.connection
from flask import jsonify, request, Response
from config import Config
from db import Db


class Venues:
    def __init__(self):
        return None

    def date_handler(self, obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            else:
                raise TypeError

    def defaultencode(self,o):
        if isinstance(o, Decimal):
            return fakefloat(o)
        raise TypeError(repr(o) + " is not JSON serializable")


    def getVenues(self):
        
        event = request.args.get('event') if request.args.get('event') is not None else None
        category = request.args.get('category') if request.args.get('category') is not None else None
        #name = request.args.get('name') if request.args.get('name') is not None else None
        count = request.args.get('count') if request.args.get('count') is not None else None
        event_id = None

        query = "SELECT * from venues";

        #if name is not None:
        #    query = query + " as v where v.name='"+name+"'";

        if event is not None:
            query = query + " as v JOIN events as e where v.id=e.venue_id AND e.event_name='"+event+"'";

        if category is not None:
            query = query + " as v JOIN events as e where v.id=e.venue_id AND e.category='"+category+"'";

        if count is not None:
             query = query + " LIMIT "+str(count);

        query = "SELECT * from venues"

        dbi = Db();
        data = dbi.getQuery(query);

        if category is not None and len(data) == 0:
            # Try a second query with lower case letters 
            query = query + " as v JOIN events as e where v.id=e.venue_id AND e.event_name='"+category.lower()+"';"
            data = dbi.getQuery(query);

        elif event is not None and len(data) == 0:
            # Try a second query with lower case letters 
            query = query + " as v JOIN events as e where v.id=e.venue_id AND e.event_name='"+event.lower()+"';"
            data = dbi.getQuery(query)

        results = {}
        if len(data) >= 1:
            for row, values in enumerate(data):
                print(str(values))
                results[row] = {
                    'id':values[0],
                    'venue_name':values[1],
                    'lat':str(values[2]),
                    'long':str(values[3]),
                    'date_added':self.date_handler(values[4]),
                    'date_updated':self.date_handler(values[5]),
                }

        if len(data) >= 13:
            for row, values in enumerate(data):
                print(str(values))
                results[row]['category'] = values[14]

        return jsonify(results)

    def getVenue(self,venuename):

        query = "SELECT * from venues where name='" + venuename + "';"

        dbi = Db();
        data = dbi.getQuery(query);

        results = {}
        if len(data)>=1:
            for row, values in enumerate(data):
                results = {'id':values[0],
                   'venuename':values[1],
                   'lat':str(values[2]),
                   'long':str(values[3]),
                   'date_added':self.date_handler(values[4]),
                   'date_updated':self.date_handler(values[5])
                }

        return jsonify(data=results)

# class fakefloat(float):
#     def __init__(self, value):
#         self._value = value
#     def __repr__(self):
#         return str(self._value)
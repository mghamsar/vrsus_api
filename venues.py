import MySQLdb
import boto, boto.s3.connection
from flask import jsonify, request, Response
from config import Config


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
        cursor = Config.dbConnect.cursor()

        query = "SELECT * from venues"

        event = request.args.get('event') if request.args.get('event') is not None else None
        category = request.args.get('category') if request.args.get('category') is not None else None
        event_id = None

        if event is not None:
            query = query + " as v JOIN events as e where v.id=e.venue_id AND e.event_name='"+event+"'"

        if category is not None:
            query = query + " as v JOIN events as e where v.id=e.venue_id AND e.category='"+category+"'"

        query = query +";"

        try:
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                return "The request did return results"
            except IndexError:
                print "MySQL Error: %s" % str(e)
                return None

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

    def getInfo(self,venuename):
        cursor = Config.dbConnect.cursor()

        # Get values from query string
        event = request.args.get('event') if request.args.get('event') is not None else None

        results = {}
        try:
            cursor.execute("SELECT * from venues where name='" + venuename + "'")
            data = cursor.fetchall()

            for row, values in enumerate(data):
                results = {'id':values[0],
                   'venuename':values[1],
                   'lat':str(values[2]),
                   'long':str(values[3]),
                   'date_added':self.date_handler(values[4]),
                   'date_updated':self.date_handler(values[5])
                }
            if results is None:
                return "Venue name did not return any results"
            else:
                return jsonify(data=results)

        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                return None
            except IndexError:
                print "MySQL Error: %s" % str(e)
                return None
        except TypeError, e:
            print(e)
            return None
        except ValueError, e:
            print(e)
            return None
        finally:
            cursor.close()
            Config.dbConnect.close()

# class fakefloat(float):
#     def __init__(self, value):
#         self._value = value
#     def __repr__(self):
#         return str(self._value)
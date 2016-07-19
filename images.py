import MySQLdb
import boto, boto.s3.connection
from flask import jsonify, request, Response, make_response
from config import Config
import json

class Images:

    def date_handler(self, obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            else:
                raise TypeError

    def loadImage(self, imagename):
        conn = boto.connect_s3(aws_access_key_id = Config.S3_ACCESS_KEY, aws_secret_access_key = Config.S3_SECRET_KEY)
        bucket = conn.get_bucket('vrsusimages', validate=False)
        key = boto.s3.key.Key(bucket)
        key.key = imagename 

        try:
            key.open_read()
            headers = dict(key.resp.getheaders())
            return Response(key, headers=headers)
        except boto.exception.S3ResponseError as e:
            return Response(e.body, status=e.status, headers=key.resp.getheaders())

    def getImageNames(self):
        
        eventName = request.args.get('eventname') if request.args.get('eventname') is not None else None
        count = request.args.get('count') if request.args.get('count') is not None else None
        order = request.args.get('order') if request.args.get('order') is not None else None

        query = "SELECT * from images"

        if eventName is not None: 
            query = query + " where " + "event_name='" + eventName

        if order is not None:
            query = query + " ORDER BY date_updated " + order
        
        if count is not None: 
            query = query + " LIMIT " + count

        query = query +";"

        cursor = Config.dbConnect.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchall()
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                return None
            except IndexError:
                print "MySQL Error: %s" % str(e)
                return None 
            
        results = {}
        responses = []
        if len(data) >= 1:
            for row, values in enumerate(data):
                results[row] = {
                    'id':values[0],
                    'file_name':values[1],
                    'type': values[2],
                    'venue_id':values[3],
                    'venue_name':values[4],
                    'event_id':values[5],
                    'event_name':values[6],
                    'date_added':self.date_handler(values[7]),
                    'date_updated':self.date_handler(values[8])
                }

                responses.append(results[row]['file_name'])

            return jsonify(data=responses)
        else:
            return "No Image Ids Found with the Specified Search"
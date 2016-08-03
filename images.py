import MySQLdb
import os, time
import boto, boto.s3.connection
from flask import jsonify, request, redirect, url_for, Response, make_response
from config import Config
import json
from db import Db
import cStringIO
import urllib
import Image

class Images:

    def date_handler(self, obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            else:
                raise TypeError

    def loadImage(self, filename):
        conn = boto.connect_s3(aws_access_key_id = Config.S3_ACCESS_KEY, aws_secret_access_key = Config.S3_SECRET_KEY)
        bucket = conn.get_bucket('vrsusimages', validate=False)
        key = boto.s3.key.Key(bucket)
        key.key = filename 

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

        dbi = Db();
        data = dbi.getQuery(query);
    
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


    def addImage(self,imagename, eventname=None, venuename=None):
        s3 = boto.connect_s3(aws_access_key_id = Config.S3_ACCESS_KEY, aws_secret_access_key = Config.S3_SECRET_KEY)
        bucket = s3.get_bucket('vrsusimages', validate=False)
        k = boto.s3.key.Key(bucket)

        # Loop over the list of files from the HTML input control
        data_files = request.files.getlist('image[]')
        
        for data_file in data_files:
            file_contents = data_file.read()
            size = len(file_contents)

            #k.key = data_file.filename
            k.key = imagename
            sent = k.set_contents_from_string(file_contents)

            if sent == size:
                self.addImageToDb(imagename, eventname, venuename)

                return redirect(url_for('.get_images'))

            else:
                return "Could not upload image"

    
    def addImageToDb(self, imagename, eventname=None, venuename=None, category=None):

        now = time.strftime('%Y-%m-%d')
        query = "SELECT name from images where name='"+imagename+"';"
        dbi = Db();
        data = dbi.getQuery(query);

        if not data:
            addquery = "INSERT INTO images(id,name,date_added,date_updated) VALUES ('','"+imagename+"','"+now+"','"+now+"');"
            print addquery

            dbi.addQuery(addquery);

        elif eventname is not None:
            addquery = "UPDATE videos SET event_name='"+eventname+"' WHERE name='"+imagename+"';"

            dbi.addQuery(addquery);

        return 0
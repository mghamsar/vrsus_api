import MySQLdb
import os, time, json
import boto, boto.s3.connection
from flask import jsonify, request, redirect, url_for, Response, make_response
from config import Config
from db import Db
import events
import videos
import collections

class Images:

    event = events.Events();
    video = videos.Videos();

    def date_handler(self, obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            else:
                raise TypeError

    def loadImage(self, filename):
        conn = boto.connect_s3(aws_access_key_id = Config.S3_ACCESS_KEY, aws_secret_access_key = Config.S3_SECRET_KEY)
        bucket = conn.get_bucket('vrsusimages', validate=False)
        key = boto.s3.key.Key(bucket)
        filename = filename.lower()
        key.key = filename

        try:
            key.open_read()
            headers = dict(key.resp.getheaders())
            if headers['content-type'] is not 'image/jpeg': 
                headers['content-type'] = 'image/jpeg'

            return Response(key, headers=headers)
        except boto.exception.S3ResponseError as e:
            return Response(e.body, status=e.status, headers=key.resp.getheaders())


    def getCategoryImages(self):

        query = "SELECT id,name,category from images where type='category' ORDER BY position;"
        dbi = Db();
        data = dbi.getQuery(query);

        results = {}
        if len(data) >= 1:
            for row, values in enumerate(data):
                results[row] = {
                    'id':values[0],
                    'file_name':values[1],
                    'category':values[2]
                }

        return jsonify(data=results)



    def getImageNames(self):

        category = request.args.get('category') if request.args.get('category') is not None else None
        if category is not None and int(category) == 1:
            return self.getCategoryImages()

        else:
            eventName = request.args.get('event') if request.args.get('event') is not None else None
            count = request.args.get('count') if request.args.get('count') is not None else None
            order = request.args.get('order') if request.args.get('order') is not None else None

            query = "SELECT id,name,category from images"

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
                        'category':values[2]
                    }

                    responses.append(results[row]['file_name'])

            return jsonify(data=results)


    def addImage(self,imagename=None, eventname=None, venuename=None):
        s3 = boto.connect_s3(aws_access_key_id = Config.S3_ACCESS_KEY, aws_secret_access_key = Config.S3_SECRET_KEY)
        bucket = s3.get_bucket('vrsusimages', validate=False)
        k = boto.s3.key.Key(bucket)

        # Loop over the list of files from the HTML input control
        data_files = request.files.getlist('image[]')
        imagename = request.form['image_name']
        
        for data_file in data_files:
            file_contents = data_file.read()
            size = len(file_contents)

            if len(imagename)<=1:
                imagename = data_file.filename

            imagename = imagename.lower()
            k.key = imagename
            print "Uploading some data to bucket with key: " + k.key
            sent = k.set_contents_from_string(file_contents)

            if sent == size:
                self.addImageToDb(k.key, eventname, venuename)

                return redirect(url_for('.get_images'))

            else:
                return "Could not upload image"

    
    def addImageToDb(self, imagename, eventname=None, venuename=None, category=None):

        now = time.strftime('%Y-%m-%d')
        query = "SELECT name from images where name='"+imagename+"';"
        dbi = Db();
        data = dbi.getQuery(query);

        eventData = self.event.updateEvent(eventname,eventtype,eventcategory)
        print "EVENT ID", eventData
        event_id, event_name = eventData[0]

        if not data:
            addquery = "INSERT INTO images(id,name,date_added,date_updated) VALUES ('','"+imagename+"','"+now+"','"+now+"');"
            print addquery

            dbi.addQuery(addquery);

        elif eventname is not None:
            addquery = "UPDATE videos SET event_name='"+eventname+"' WHERE name='"+imagename+"';"

            dbi.addQuery(addquery);

        return 0
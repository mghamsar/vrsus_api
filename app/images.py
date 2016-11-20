from app import models,db
from flask import request, jsonify, redirect, url_for, Response

import boto, boto.s3.connection
import config
import time

class Images:

    def getImageNames(self):

        category = request.args.get('category') if request.args.get('category') is not None else None
        event = request.args.get('event') if request.args.get('event') is not None else None
        count = request.args.get('count') if request.args.get('count') is not None else None
        
        if category is not None and int(category) == 1:
            images = models.ImagesData.query.filter_by(type='category').all()

        else:
            images = models.ImagesData.query.all()
            if event is not None:
                ev = models.EventsData.query.filter_by(event_name=event).first()
                images = models.ImagesData.query.filter_by(event_id=ev.event_id).all()

            if count is not None:
                images = models.ImagesData.query.limit(int(count)).all()

        results = {}
        for row, value in enumerate(images):
            results[row] = {
                'id':value.id,
                'file_name':value.image_name,
                'category':value.category
            }

        return jsonify(data=results)


    def loadImage(self, filename):

        # Call CloudFront Endpoint
        # url = "http://d396uhl77uxno9.cloudfront.net"+"/"+filename 
        # return redirect(url, code=302)
        conn = boto.connect_s3(aws_access_key_id = config.S3_ACCESS_KEY, aws_secret_access_key = config.S3_SECRET_KEY)
        bucket = conn.get_bucket('vrsusimages', validate=False)
        key = boto.s3.key.Key(bucket)
        filename = filename.lower()
        
        for i, key in enumerate(bucket.list()):
            if key.name == filename:
                key.key = filename
                
                try:
                    key.open_read()
                    headers = dict(key.resp.getheaders())
                    if headers['content-type'] is not 'image/jpeg': 
                        headers['content-type'] = 'image/jpeg'
                    return Response(key, headers=headers)
                except boto.exception.S3ResponseError as e:
                    return Response(e.body, status=e.status, headers=key.resp.getheaders())

        return "Image not found on server"

    def addImage(self,image_files, imagename=None, video_id=None, eventname=None,category=None, type=None):
        s3 = boto.connect_s3(aws_access_key_id = config.S3_ACCESS_KEY, aws_secret_access_key = config.S3_SECRET_KEY)
        bucket = s3.get_bucket('vrsusimages', validate=False)
        k = boto.s3.key.Key(bucket)

        # # Loop over the list of files from the HTML input control
        # data_files = request.files.getlist('image[]')
        # imagename = request.form['image_name']
        # eventname = request.form['image_event_name']
        
        for data_file in image_files:
            file_contents = data_file.read()
            size = len(file_contents)

            if len(imagename)<=1:
                imagename = data_file.filename

            imagename = imagename.lower()
            k.key = imagename
            print "Uploading some data to bucket with key: " + k.key
            sent = k.set_contents_from_string(file_contents)

            if sent == size:
                self.addImageToDb(k.key, video_id=video_id, eventname=eventname, category=category, type=type)

                return redirect(url_for('.get_images'))

            else:
                return "Could not upload image"


    def addImageToDb(self, imagename, video_id=None, eventname=None, category=None, type=None):
        
        now = time.strftime('%Y-%m-%d')
        img = models.ImagesData.query.filter_by(image_name=imagename).first()

        if img is not None and imagename == img.image_name:
            if eventname is not None:
                ev = models.EventsData.query.filter_by(event_name=eventname).first()
                if ev.event_id is not None: 
                    img.event_id = ev.event_id
            
            if video_id is not None: 
                img.video_id=video_id
            if category is not None: 
                img.category=category
            if type is not None: 
                img.type=type

        else:
            print "img not found", imagename
            if eventname is not None:
                ev = models.EventsData.query.filter_by(event_name=eventname).first()
                img = models.ImagesData(imagename, video_id=video_id, event_id=ev.event_id, event_name=ev.event_name, date_added=now, date_updated=now)
            else: 
                print "No event name provided"
                img = models.ImagesData(imagename, video_id=video_id, date_added=now, date_updated=now)

        db.session.add(img)
        db.session.commit()
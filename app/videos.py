from app import models,db
from flask import request, jsonify, redirect, url_for

import boto, boto.s3.connection
import config
import time, json

class Videos:

    def getVideos(self, template=False):
        
        event = request.args.get('event') if request.args.get('event') is not None else None
        count = request.args.get('count') if request.args.get('count') is not None else None
        order = request.args.get('order') if request.args.get('order') is not None else None

        ev = models.EventsData.query.filter_by(event_name=event).first()

        videos = models.VideosData.query.all()

        if event is not None: 
            videos = models.VideosData.query.filter_by(event_id=ev.event_id)

        if count is not None:
            videos = models.videosData.query.limit(int(count)).all()

        results = {}
        if len(data) >= 1:            
            for row, values in enumerate(data):
                results[row] = {
                    'id':values[0],
                    'video_name':values[1],
                    'type': values[2],
                    'event_id':values[3],
                    'event_name':values[4],
                    'category':values[7],
                    'date_added':self.date_handler(values[5]),
                    'date_updated':self.date_handler(values[6])
                }
        
        if template==True:
            return json.loads(json.dumps(results))#json.dumps(results, sort_keys=True,)

        return jsonify(results)

    def getVideo(self, videoname):
        s3 = boto.connect_s3(aws_access_key_id = Config.S3_ACCESS_KEY, aws_secret_access_key = Config.S3_SECRET_KEY)
        bucket = s3.get_bucket('vrsuscovideos')
        key = boto.s3.key.Key(bucket)
        videoname = videoname.lower()

        for i, key in enumerate(bucket.list()):
            if key.name == videoname:
                key.key = videoname

                try:
                    key.open_read()
                    headers = dict(key.resp.getheaders())
                    #headers['content-type'] = 'video/mp4'
                    return Response(key, headers=headers)
                except boto.exception.S3ResponseError as e:
                    return Response(e.body, status=e.status, headers=key.resp.getheaders())
        
        return "Video not found on server"


    def addVideo(self,videoname=None, eventname=None, venuename=None):
        s3 = boto.connect_s3(aws_access_key_id = Config.S3_ACCESS_KEY, aws_secret_access_key = Config.S3_SECRET_KEY)
        bucket = s3.get_bucket('vrsuscovideos')
        k = Key(bucket)

        # Loop over the list of files from the HTML input control
        data_files = request.files.getlist('file[]')
        videoname = request.form['video_name'] if request.form['video_name'] is not None else None
        eventname = request.form['event_name'] if request.form['event_name'] is not None else None
        eventtype = request.form['event_type'] if request.form['event_type'] is not None else None
        eventcategory = request.form["event_category"] if request.form["event_category"] is not None else None

        for data_file in data_files:

            # Read the contents of the file
            file_contents = data_file.read()
            
            try:
                size = os.fstat(data_file.fileno()).st_size
            except:
                # Not all file objects implement fileno(), so we fall back on this
                data_file.seek(0, os.SEEK_END)
                size = data_file.tell()

            if videoname is None:
                videoname = data_file.filename

            videoname = videoname.lower()
            videoname = videoname.replace(" ","_")
            k.key = videoname

            # Use Boto to upload the file to the S3 bucket
            print "Uploading some data to bucket with key: " + k.key
            sent = k.set_contents_from_string(file_contents)

            if sent == size:
                self.addVideoToDb(videoname, eventname, eventtype, eventcategory)

                return redirect(url_for('.get_videos'))

            else:
                return "Could not upload Video"


    def addVideoToDb(self, videoname, eventname=None, eventtype=None, eventcategory=None):

        now = time.strftime('%Y-%m-%d')
        video = models.VideosData.query.filter_by(name=videoname).first()

        if video is not None and videoname == video.name:
            if eventname is not None:
                ev = models.EventsData.query.filter_by(event_name=eventname).first()
                if ev.event_id is not None:
                    video.event_id = ev.event_id
        else:
            if eventname is not None:
                ev = models.EventsData.query.filter_by(event_name=eventname).first()
                video = models.VideosData(videoname, event_id=ev.event_id, date_added=now, date_updated=now)

            else: 
                print "No event name"
                video = models.VideosData(videoname, date_added=now, date_updated=now)

        db.session.add(img)
        db.session.commit()


    # def getCategories(self):
    #     query = "SELECT DISTINCT category from videos;"
    #     dbi = Db();
    #     data = dbi.getQuery(query);

    #     results = {}
    #     if len(data) >= 1:            
    #         for row, values in enumerate(data):
    #             results[row] = {
    #                 'cat':values[0],
    #             }
        
    #     return json.loads(json.dumps(results))


    # def getTypes(self):
    #     query = "SELECT DISTINCT type from videos;"
    #     dbi = Db();
    #     data = dbi.getQuery(query);

    #     results = {}
    #     if len(data) >= 1:            
    #         for row, values in enumerate(data):
    #             results[row] = {
    #                 'type':values[0],
    #             }
        
    #     return json.loads(json.dumps(results))
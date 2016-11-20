from app import models,db,images, audio
from flask import request, jsonify, redirect, url_for, Response
from boto.s3.key import Key
import boto, boto.s3.connection
import config
import time, json, os

class Videos:

    def date_handler(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError

    def getVideos(self, template=False):
        
        event = request.args.get('event') if request.args.get('event') is not None else None
        count = request.args.get('count') if request.args.get('count') is not None else None
        order = request.args.get('order') if request.args.get('order') is not None else None
        category = request.args.get('category') if request.args.get('category') is not None else None

        videos = models.VideosData.query

        if event is not None:
            ev = models.EventsData.query.filter_by(event_name=event).first()
            if ev:
                videos = videos.filter_by(event_id=ev.event_id)
        if category is not None:
            videos = videos.filter_by(category=category)

        if count is not None:
            videos = videos.limit(int(count))

        videos = videos.all()

        results = {}
        if videos:            
            for row, values in enumerate(videos):
                results[row] = {
                    'id':values.video_id,
                    'video_name':values.video_name,
                    'type': values.type,
                    'event_id':values.event_id,
                    'event_name':values.event_name,
                    'category':values.category,
                    'date_added':self.date_handler(values.date_added),
                    'date_updated':self.date_handler(values.date_updated)
                }
        
        if template==True:
            return json.loads(json.dumps(results))

        return jsonify(results)

    def getVideo(self, videoname):
        s3 = boto.connect_s3(aws_access_key_id = config.S3_ACCESS_KEY, aws_secret_access_key = config.S3_SECRET_KEY)
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

    #def videoStream(self, video):
        

    def addVideo(self):
        
        video_files = request.files.getlist('video[]')
        audio_files = request.files.getlist('audio[]')
        image_files = request.files.getlist('image[]')
        videoname = request.form['video_name'] if request.form['video_name'] is not None else None
        imagename = request.form['image_name'] if request.form['image_name'] is not None else None
        audioname = request.form['audio_name'] if request.form['audio_name'] is not None else None
        eventname = request.form['event_name'] if request.form['event_name'] is not None else None
        eventtype = request.form['event_type'] if request.form['event_type'] is not None else None
        eventcategory = request.form["event_category"] if request.form["event_category"] is not None else None

        self.addVideotoStorage(video_files,videoname,eventname,eventtype,eventcategory)

        # Update images DB and Storage
        img = images.Images()
        v = models.VideosData.query.filter_by(video_name=videoname).first()
        if v is not None: 
            print v.video_id
            img.addImage(image_files,imagename,video_id=v.video_id,eventname=eventname,category=eventcategory,type=eventtype)
        else: 
            img.addImage(image_files,imagename,eventname=eventname,category=eventcategory,type=eventtype)


        # UPDATE Audio DB and Storage
        aud = audio.Audio()
        # aud.addAudio(audio_files,audioname,eventname,eventtype,eventcategory)

        return redirect(url_for('.get_videos'))
            

    def addVideotoStorage(self,video_files, videoname=None, eventname=None, eventtype=None, eventcategory=None):

        s3 = boto.connect_s3(aws_access_key_id = config.S3_ACCESS_KEY, aws_secret_access_key = config.S3_SECRET_KEY)
        bucket = s3.get_bucket('vrsuscovideos')
        k = Key(bucket)

        for video_file in video_files:
            print video_file
            # Read the contents of the file
            file_contents = video_file.read()
            
            try:
                size = os.fstat(video_file.fileno()).st_size
            except:
                # Not all file objects implement fileno(), so we fall back on this
                video_file.seek(0, os.SEEK_END)
                size = video_file.tell()

            if videoname is None:
                videoname = video_file.filename

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
        video = models.VideosData.query.filter_by(video_name=videoname).first()

        if video is not None and videoname == video.video_name:
            if eventname is not None:
                ev = models.EventsData.query.filter_by(event_name=eventname).first()
                if ev is not None:
                    video.event_id = ev.event_id
                    video.event_name = ev.event_name
                else:
                    ev2 = models.EventsData(eventname, date_added=now, date_updated=now)
                    db.session.add(ev2)
                    db.session.commit()
                    ev2 = models.EventsData.query.filter_by(event_name=eventname).first()
                    video = models.VideosData(videoname, event_id=ev2.event_id, event_name=ev2.event_name, type=eventtype, category=eventcategory, date_added=now, date_updated=now)

        else:
            if eventname is not None:
                ev = models.EventsData.query.filter_by(event_name=eventname).first()
                if ev is not None: 
                    video = models.VideosData(videoname, event_id=ev.event_id, event_name=ev.event_name, type=eventtype, category=eventcategory, date_added=now, date_updated=now)
                else: 
                    ev2 = models.EventsData(eventname, date_added=now, date_updated=now)
                    db.session.add(ev2)
                    db.session.commit()
                    ev2 = models.EventsData.query.filter_by(event_name=eventname).first()
                    video = models.VideosData(videoname, event_id=ev2.event_id, event_name=ev2.event_name, type=eventtype, category=eventcategory, date_added=now, date_updated=now)
            else: 
                print "No event name"
                video = models.VideosData(videoname, date_added=now, date_updated=now)

        db.session.add(video)
        db.session.commit()

    def getCategories(self):
                
        data = db.session.query(models.VideosData.category.distinct().label("category")).all()
        results = {}
        if data:            
            for row,value in enumerate(data):
                results[row] = {
                    'cat':str(value[0].encode("utf-8")),
                }
        return json.loads(json.dumps(results))

    def getTypes(self):
        
        data = db.session.query(models.VideosData.type.distinct().label("type")).all()
        results = {}
        if data:            
            for row, value in enumerate(data):
                results[row] = {
                    'type':value[0].encode("utf-8"),
                }
        return json.loads(json.dumps(results))
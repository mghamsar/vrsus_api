import MySQLdb
import os, time, json
import boto, boto.s3.connection
from boto.s3.key import Key
from flask import jsonify, url_for, request, redirect, Response,render_template
from config import Config
from db import Db
import events

class Videos:

    event = events.Events();

    def date_handler(self, obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            else:
                raise TypeError

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
        query = "SELECT name from videos where name='"+videoname+"';"
        dbi = Db();
        videodata = dbi.getQuery(query);

        eventData = self.event.updateEvent(eventname,eventtype,eventcategory)
        print "EVENT ID", eventData
        event_id, event_name = eventData[0]

        
        if videodata:
            if eventtype is not None and eventcategory is not None:
                addquery = "UPDATE videos SET event_id="+str(event_id)+", event_name='"+event_name+"', type='"+eventtype+"', category='"+eventcategory+"',\
                date_updated='"+now+"' WHERE name='"+videoname+"';"

                print addquery
                dbi.addQuery(addquery);
                  
            elif eventtype is not None: 
                addquery = "UPDATE videos SET event_id="+str(event_id)+", event_name='"+event_name+"', type='"+eventtype+"', date_updated='"+now+"' WHERE name='"+videoname+"';"
                
                print addquery
                dbi.addQuery(addquery);

        else:
            if eventtype is not None and eventcategory is not None:
                addvideoquery = "INSERT INTO videos VALUES \
                (NULL,'"+videoname+"','"+eventtype+"',"+str(event_id)+",'"+event_name+"','"+now+"','"+now+"','"+eventcategory+"');"
                dbi.addQuery(addvideoquery);
            elif eventtype is not None:
                addvideoquery = "INSERT INTO videos VALUES \
                (NULL,'"+videoname+"','"+eventtype+"',"+str(event_id)+",'"+event_name+"','"+now+"','"+now+"',NULL);"
                dbi.addQuery(addvideoquery);
        
        return 0

    def getVideos(self, template=False):
        
        event = request.args.get('event') if request.args.get('event') is not None else None
        count = request.args.get('count') if request.args.get('count') is not None else None
        order = request.args.get('order') if request.args.get('order') is not None else None

        query = "SELECT * from videos"

        if event is not None: 
            query = query + " where " + "event_name='" + event + "'"

        if order is not None:
            query = query + " ORDER BY date_updated " + order
        
        if count is not None: 
            query = query + " LIMIT " + count

        query = query +";"
        dbi = Db();
        data = dbi.getQuery(query);

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

    def getCategories(self):
        query = "SELECT DISTINCT category from videos;"
        dbi = Db();
        data = dbi.getQuery(query);

        results = {}
        if len(data) >= 1:            
            for row, values in enumerate(data):
                results[row] = {
                    'cat':values[0],
                }
        
        return json.loads(json.dumps(results))


    def getTypes(self):
        query = "SELECT DISTINCT type from videos;"
        dbi = Db();
        data = dbi.getQuery(query);

        results = {}
        if len(data) >= 1:            
            for row, values in enumerate(data):
                results[row] = {
                    'type':values[0],
                }
        
        return json.loads(json.dumps(results))


# ALTERNATE WAY OF GETTING A FILE WITH HEADERs
# key = bucket.get_key(videoname)
        # key.get_contents_to_filename(videoname)
        # if key:        
        #     with open(videoname, 'rb') as f:
        #         body = f.read()
        #         response = make_response(body)
        #         response.headers['Content-Description'] = 'File Transfer'
        #         response.headers['Cache-Control'] = 'no-cache'
        #         response.headers['Content-Type'] = 'video/mp4'
        #         response.headers['Accept-Ranges'] = 'bytes'
        #         response.headers['Access-Control-Allow-Origin'] = '*'
        #         response.headers['Content-Disposition'] = 'inline; filename=%s' %videoname
        #     return response
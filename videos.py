import MySQLdb
import boto, boto.s3.connection
from flask import jsonify, request, Response
from config import Config

class Videos:

    def date_handler(self, obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            else:
                raise TypeError

    def getVideo(self, videoname):
        s3 = boto.connect_s3(aws_access_key_id = Config.S3_ACCESS_KEY, aws_secret_access_key = Config.S3_SECRET_KEY)
        bucket = s3.get_bucket('vrsuscovideos')
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

        key = boto.s3.key.Key(bucket)
        key.key = videoname 

        try:
            key.open_read()
            headers = dict(key.resp.getheaders())
            #headers['content-type'] = 'video/mp4'
            return Response(key, headers=headers)
        except boto.exception.S3ResponseError as e:
            return Response(e.body, status=e.status, headers=key.resp.getheaders())   

    def getVideos(self):
        conn = MySQLdb.connect( host=Config.MYSQL_DATABASE_HOST,
                            user=Config.MYSQL_DATABASE_USER,
                            passwd=Config.MYSQL_DATABASE_PASSWORD,
                            db=Config.MYSQL_DATABASE_DB,
                            port=Config.MYSQL_DATABASE_PORT)
        
        cursor = conn.cursor()
        eventName = request.args.get('eventname') if request.args.get('eventname') is not None else None

        if eventName is not None:
            try:
                cursor.execute("SELECT * from videos where event_name='" + eventName + "';")
                data = cursor.fetchall()

            except MySQLdb.Error, e:
                try:
                    print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                    return None
                except IndexError:
                    print "MySQL Error: %s" % str(e)
                    return None 

        else:
            try:
                cursor.execute("SELECT * from videos ORDER BY date_added LIMIT 20;")
                data = cursor.fetchall()

            except MySQLdb.Error, e:
                try:
                    print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                    return None
                except IndexError:
                    print "MySQL Error: %s" % str(e)
                    return None 
            
            print "Fetching all data, no event filter specified"

        if len(data) >= 1:            
            for row, values in enumerate(data):
                results = {
                    'id':values[0],
                    'video_name':values[1],
                    'type': values[2],
                    'video_id':values[3],
                    'event_id':values[4],
                    'event_name':values[5],
                    'venue_name':values[7],
                    'date_added':self.date_handler(values[6]),
                    'date_updated':self.date_handler(values[8])
                }

                s3 = boto.connect_s3(aws_access_key_id = Config.S3_ACCESS_KEY, aws_secret_access_key = Config.S3_SECRET_KEY)
                bucket = s3.get_bucket('vrsuscovideos')
            
                print results['video_name']
                key = boto.s3.key.Key(bucket)
                key.key = results['video_name']

                try:
                    key.open_read()
                    headers = dict(key.resp.getheaders())
                    headers['content-type'] = 'video/mp4'
                    return Response(key, headers=headers)
                except boto.exception.S3ResponseError as e:
                    return Response(e.body, status=e.status, headers=key.resp.getheaders())

        else:
            return "No Videos Found with the Specified Search"

        
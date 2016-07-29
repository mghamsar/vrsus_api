import MySQLdb
import os, time
import boto, boto.s3.connection
from boto.s3.key import Key
from flask import jsonify, url_for, request, redirect, Response,render_template
from config import Config
from db import Db

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

    def addVideo(self,filename,data_file):
        s3 = boto.connect_s3(aws_access_key_id = Config.S3_ACCESS_KEY, aws_secret_access_key = Config.S3_SECRET_KEY)
        bucket = s3.get_bucket('vrsuscovideos')
        k = Key(bucket)

        # Loop over the list of files from the HTML input control
        data_files = request.files.getlist('file[]')
        for data_file in data_files:

            try:
                size = os.fstat(data_file.fileno()).st_size
            except:
                # Not all file objects implement fileno(),
                # so we fall back on this
                file.seek(0, os.SEEK_END)
                size = data_file.tell()

            # Read the contents of the file
            file_contents = data_file.read()

            # Use Boto to upload the file to the S3 bucket
            #k.key = data_file.filename
            k.key = filename
            print "Uploading some data to bucket with key: " + k.key
            sent = k.set_contents_from_string(file_contents)

            if sent == size:
                #self.addVideoToDb(filename)
                now = time.strftime('%Y-%m-%d')
                query = "INSERT INTO videos(id,name,date_added,date_updated) VALUES ('','"+filename+"','"+now+"','"+now+"');"
                

                dbConnect = MySQLdb.connect(host=Config.MYSQL_DATABASE_HOST, user=Config.MYSQL_DATABASE_USER, 
                    passwd=Config.MYSQL_DATABASE_PASSWORD,
                    db=Config.MYSQL_DATABASE_DB,
                    port=Config.MYSQL_DATABASE_PORT)
        
                cursor =dbConnect.cursor()
                
                try:
                    cursor.execute(query)
                    Config.dbConnect.commit()

                except MySQLdb.Error, e:
                    try:
                        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                        return None
                    except IndexError:
                        print "MySQL Error: %s" % str(e)
                        return None
                finally:
                    cursor.close()
                    dbConnect.close()

                return redirect(url_for('.get_videos'))

            else:
                return "Could not upload Video"

    
    def addVideoToDb(self, videoname):

        now = time.strftime('%Y-%m-%d')
        query = "INSERT INTO videos(id,name,date_added,date_updated) VALUES ('','"+videoname+"',"+now+","+now+");"

        print query

        dbConnect = MySQLdb.connect(host=Config.MYSQL_DATABASE_HOST, user=Config.MYSQL_DATABASE_USER, 
            passwd=Config.MYSQL_DATABASE_PASSWORD,
            db=Config.MYSQL_DATABASE_DB,
            port=Config.MYSQL_DATABASE_PORT)
        
        cursor =dbConnect.cursor()

        try:
            cursor.execute(query)

        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                return None
            except IndexError:
                print "MySQL Error: %s" % str(e)
                return None
        finally:
            cursor.close()
            dbConnect.close()

        return 0

    def getVideos(self):
        
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
                print(values[6])
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

        return jsonify(results)
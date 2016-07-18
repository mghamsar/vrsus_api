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

    def getImage(self, imagename):
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


    def getInfo(self,venuename):
        conn = MySQLdb.connect( host=Config.MYSQL_DATABASE_HOST,
                                user=Config.MYSQL_DATABASE_USER,
                                passwd=Config.MYSQL_DATABASE_PASSWORD,
                                db=Config.MYSQL_DATABASE_DB,
                                port=Config.MYSQL_DATABASE_PORT)
        cursor = conn.cursor()

        # Get values from query string
        video_name = request.args.get('video');

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
            conn.close()

# class fakefloat(float):
#     def __init__(self, value):
#         self._value = value
#     def __repr__(self):
#         return str(self._value)
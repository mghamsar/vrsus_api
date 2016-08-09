import MySQLdb
import boto, boto.s3.connection
from flask import jsonify, request, Response, make_response
from config import Config
import json

class Audio3D:

    def date_handler(self, obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            else:
                raise TypeError

    def showAudioData(self):
        conn = boto.connect_s3(aws_access_key_id = Config.S3_ACCESS_KEY, aws_secret_access_key = Config.S3_SECRET_KEY)
        bucket = conn.get_bucket('3daudiofiles', validate=False)

        results = {}
        for i, key in enumerate(bucket.list()):
            results[i] = key.name.encode('utf-8')

        return jsonify(results)

    def loadAudio(self,filename):
        conn = boto.connect_s3(aws_access_key_id = Config.S3_ACCESS_KEY, aws_secret_access_key = Config.S3_SECRET_KEY)
        bucket = conn.get_bucket('3daudiofiles', validate=False)
        key = boto.s3.key.Key(bucket)

        filename = filename.lower()
        key.key = filename

        try:
            key.open_read()
            headers = dict(key.resp.getheaders())
            return Response(key, headers=headers)
        except boto.exception.S3ResponseError as e:
            return Response(e.body, status=e.status, headers=key.resp.getheaders())
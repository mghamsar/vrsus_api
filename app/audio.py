import boto
import boto.s3.connection
from boto.s3.key import Key
from flask import jsonify, request, redirect, Response, url_for
import config
import os


class Audio:

    def date_handler(self, obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            else:
                raise TypeError

    def showAudioData(self):
        conn = boto.connect_s3(
            aws_access_key_id=config.S3_ACCESS_KEY,
            aws_secret_access_key=config.S3_SECRET_KEY)
        bucket = conn.get_bucket('3daudiofiles', validate=False)

        results = {}
        for i, key in enumerate(bucket.list()):
            results[i] = key.name.encode('utf-8')

        return jsonify(results)

    def loadAudio(self, filename):
        conn = boto.connect_s3(
            aws_access_key_id=config.S3_ACCESS_KEY,
            aws_secret_access_key=config.S3_SECRET_KEY)
        bucket = conn.get_bucket('3daudiofiles', validate=False)
        key = boto.s3.key.Key(bucket)

        filename = filename.lower()
        key.key = filename

        try:
            key.open_read()
            headers = dict(key.resp.getheaders())
            return Response(key, headers=headers)
        except boto.exception.S3ResponseError as e:
            return Response(
                e.body,
                status=e.status,
                headers=key.resp.getheaders())

    def addAudio(self):
        s3 = boto.connect_s3(
            aws_access_key_id=config.S3_ACCESS_KEY,
            aws_secret_access_key=config.S3_SECRET_KEY)
        bucket = s3.get_bucket('3daudiofiles')
        k = Key(bucket)

        data_files = request.files.getlist('audio[]')
        audiofilename = request.form['audio_name'] if request.form['audio_name'] is not None else None

        for data_file in data_files:
            file_contents = data_file.read()
            try:
                size = os.fstat(data_file.fileno()).st_size
            except:
                data_file.seek(0, os.SEEK_END)
                size = data_file.tell()

            if audiofilename is None or len(audiofilename) <= 1:
                audiofilename = data_file.filename

            audiofilename = audiofilename.lower()
            audiofilename = audiofilename.replace(" ", "_")
            k.key = audiofilename

            # Use Boto to upload the file to the S3 bucket
            sent = k.set_contents_from_string(file_contents)

            if sent == size:
               # self.addAudioToDb(audiofilename, eventname, eventtype, eventcategory)
                return redirect(url_for('.get_audiofilenames'))
            else:
                return "Could not upload Audio File "+ str(audiofilename)
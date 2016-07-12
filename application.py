from flask import Flask, request, render_template, send_file, send_from_directory, make_response
from flask import Response, jsonify
from flask.json import JSONEncoder
from flask.ext.mysql import MySQL
from datetime import datetime
import boto
import json
import boto.s3.connection
import os
import tempfile
from decimal import Decimal

application = app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL()

mysql.init_app(app)

s3_access_key = 'AKIAIJP6FY37QAB4C5VA'
s3_secret_key = 's85klsigZGf5cUr+IcoaZhwNULSSMN/uqRYltDbG'

class fakefloat(float):
    def __init__(self, value):
        self._value = value
    def __repr__(self):
        return str(self._value)

@app.route("/")
def index():
	return render_template('basic.html')


@app.route('/download', methods=['POST'])
def download():
	videoname = request.form['video_name']
	return get_video(videoname)


@app.route("/video/<videoname>", methods=['GET'])
def get_video(videoname):
	s3 = boto.connect_s3(aws_access_key_id = s3_access_key, aws_secret_access_key = s3_secret_key)
	v = s3.get_bucket('vrsuscovideos').get_key(videoname)
	v.get_contents_to_filename(videoname)

	if v:
		with open(videoname, 'rb') as f:
			body = f.read()
			response = make_response(body)
			response.headers['Content-Description'] = 'File Transfer'
			response.headers['Cache-Control'] = 'no-cache'
			#response.headers['Content-Type'] = 'application/octet-stream'
			response.headers['Content-Type'] = 'video/mp4'
			#response.headers['Content-Disposition'] = 'attachment; filename=%s' % videoname
			#response.headers['X-Accel-Redirect'] = server_path

		return response

@app.route("/venues/<venuename>")
def get_venue(venuename):
	#username = request.args.get('UserName')
	#password = request.args.get('Password')

	def date_handler(obj):
	    if hasattr(obj, 'isoformat'):
	        return obj.isoformat()
	    else:
	        raise TypeError


	def defaultencode(o):
	    if isinstance(o, Decimal):
	        # Subclass float with custom repr?
	        return fakefloat(o)
	    raise TypeError(repr(o) + " is not JSON serializable")

	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from venues where name='" + venuename + "'")
	data = cursor.fetchall()

	results = {}
	for row, values in enumerate(data):
		print row, values

		results = {'id':values[0], 'venuename':values[1],
		   'lat':values[3],
		   'long':values[4],
		   'date_added':date_handler(values[5]),
		   'date_updated':date_handler(values[6])
		}

	r = results
	print r

	if results is None:
		return "Venue name did not return any results"
	else:
		return json.dumps(results,default=defaultencode)
		#jsonify(data=r)

#################---------------------###################

if __name__=="__main__":
	application.debug = True
	application.run()



from flask import Flask, request, render_template
from flask.ext.mysql import MySQL
import boto
import boto.s3.connection
import os

application = app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'vrsus'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

s3_access_key = 'AKIAIJP6FY37QAB4C5VA'
s3_secret_key = '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'
LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))

print LOCAL_PATH

#"AKIAIJP6FY37QAB4C5VA","s85klsigZGf5cUr+IcoaZhwNULSSMN/uqRYltDbG"
@app.route("/")
def index():
	return render_template('basic.html')


@app.route('/download', methods=['POST'])
def download():
	url = request.form['download_path']
	videoname = request.form['video_name']
	print url
	print videoname
	s3 = boto.connect_s3(aws_access_key_id = s3_access_key, aws_secret_access_key = s3_secret_key)
	v = s3.get_bucket('vrsuscovideos').get_key(videoname)	
	v.get_contents_to_filename(url+videoname)
	return "done"


@app.route("/video/<videoname>", methods=['GET'])
def get_video(videoname):
	s3 = boto.connect_s3(aws_access_key_id = s3_access_key, aws_secret_access_key = s3_secret_key)
	bucket = s3.get_bucket('vrsuscovideos').get_key(videoname)
#	bucket.get_contents_to_filename(videoname)
	
	return bucket

@app.route("/Authenticate")
def Authenticate():
	username = request.args.get('UserName')
	password = request.args.get('Password')
	#cursor = mysql.connect().cursor()
	#cursor.execute("SELECT * from users where Username='" + username + "' and Password='" + password + "'")
	#data = cursor.fetchone()
	return "yo"
#	if data is None:
#		return "Username or Password is wrong"
#	else:
#		return "Logged in successfully"



if __name__=="__main__":
	application.debug = True
	application.run()



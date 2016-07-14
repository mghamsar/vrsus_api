from flask import Flask, request, render_template, send_file, send_from_directory, make_response
from flask import Response, jsonify
from flask.json import JSONEncoder
#from flask.ext.mysql import MySQL
from datetime import datetime
import json
import os
import tempfile
from decimal import Decimal
import venues
import decimal
import flask.json

application = app = Flask(__name__)
app.config.from_object('config.Config')
app.json_encoder = JSONEncoder

class JSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)

@app.route("/")
def index():
    return render_template('basic.html')

@app.route('/download', methods=['POST'])
def download():
    videoname = request.form['video_name']
    return get_video(videoname)

@app.route("/video/<videoname>", methods=['GET'])
def get_video(videoname):
    venue = venues.Venues();
    return venue.getVideo(videoname) 

@app.route("/venues/<venuename>")
def get_venue(venuename):
    venue = venues.Venues();
    return venue.getInfo(venuename)
    

@app.route('/images/<imagename>', methods=['GET'])
def get_image(imagename):
    venue = venues.Venues();
    return venue.getImage(imagename)
    
#################---------------------###################

if __name__=="__main__":
    application.debug = True
    application.run()



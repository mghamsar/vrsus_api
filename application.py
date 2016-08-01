from flask import Flask, request, redirect, render_template
from flask.json import JSONEncoder
#from flask.ext.mysql import MySQL
from datetime import datetime
import json
import os
import tempfile
from decimal import Decimal
import venues
import events
import videos
import images
import decimal
import flask.json

application = app = Flask(__name__,static_folder='static', static_url_path='')
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

#################-------------------------###################

@app.route("/videos/", methods=['GET'])
def get_videos():
    v = videos.Videos()
    return v.getVideos()

@app.route("/videos/load/<videoname>", methods=['GET'])
def get_video(videoname):
    v = videos.Videos()
    return v.getVideo(videoname)

@app.route("/videos/upload", methods=['POST'])
def add_video():
    videoname = request.form['video_name']
    eventname = request.form['event_name']
    venuename = request.form['venue_name']

    v = videos.Videos()
    return v.addVideo(videoname)

##################-------------------------###################

@app.route("/events/")
def get_events():
    event = events.Events()
    return event.getEvents()

##################-------------------------###################

@app.route("/venues/")
def get_venues():
    venue = venues.Venues()
    return venue.getVenues()


@app.route("/venues/<venuename>")
def get_venue(venuename):
    venue = venues.Venues()
    return venue.getVenue(venuename)

##################-------------------------###################

@app.route("/images/", methods=['GET'])
def get_images():
    img = images.Images()
    return img.getImageNames()

@app.route('/images/load/<imagename>', methods=['GET'])
def load_image(imagename):
    img = images.Images()
    return img.loadImage(imagename)
    
#################---------------------###################

if __name__=="__main__":
    application.debug = True
    application.run()



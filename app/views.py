from flask import Flask, request, redirect, render_template, jsonify
#from flask.json import JSONEncoder
#from datetime import datetime
#from flask_sqlalchemy import SQLAlchemy
#import json, os
#import decimal
#from config import Config
#import flask.json
from app import application
#from models import ImagesData
from app import images

@application.route("/")
@application.route("/index/")
def index1():
    #v = videos.Videos()
    #data = v.getVideos(template=True)
    #categories = v.getCategories()
    #types=v.getTypes()
    return render_template('basic.html')#, videos = data, categories = categories, types=types)

# @app.route('/download', methods=['POST'])
# def download():
#     videoname = request.form['video_name']
#     return get_video(videoname)

#################-------------------------###################

# @app.route("/videos/", methods=['GET'])
# def get_videos():
#     v = videos.Videos()
#     return v.getVideos()

# @app.route("/videos/load/<videoname>", methods=['GET'])
# def get_video(videoname):
#     v = videos.V
#     return v.getVideo(videoname)

# @app.route("/videos/upload", methods=['POST'])
# def add_video():
#     v = videos.Videos()
#     return v.addVideo()

# ##################-------------------------###################

# @app.route("/events/")
# def get_events():
#     event = events.Events()
#     return event.getEvents()

# ##################-------------------------###################

# @app.route("/venues/")
# def get_venues():
#     venue = venues.Venues()
#     return venue.getVenues()


# @app.route("/venues/<venuename>")
# def get_venue(venuename):
#     venue = venues.Venues()
#     return venue.getVenue(venuename)

# ##################-------------------------###################

@application.route("/images/", methods=['GET'])
def get_images():
    img = images.Images()
    return img.getImageNames()

@application.route('/images/load/<imagename>', methods=['GET'])
def load_image(imagename):
    img = images.Images()
    return img.loadImage(imagename)

@application.route("/images/upload", methods=['POST'])
def add_image():
    img = images.Images()
    return img.addImage()
    
# #################---------------------###################

# @app.route("/audio/", methods=['GET'])
# def get_audiofilenames():
#     aud = audio3d.Audio3D()
#     return aud.showAudioData()

# @app.route('/audio/load/<audiofilename>', methods=['GET'])
# def load_audio(audiofilename):
#     aud = audio3d.Audio3D()
#     return aud.loadAudio(audiofilename)

# @app.route("/audio/upload", methods=['POST'])
# def add_audio():
#     aud = audio3d.Audio3D()
#     return aud.addAudio()

# #################---------------------###################

# if __name__=="__main__":
#     app.debug = True
#     app.run()



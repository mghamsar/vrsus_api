from flask import Flask, request, redirect, render_template, jsonify
#from config import Config
#import flask.json
from app import images, events, videos, audio
from app import application

@application.route("/")
@application.route("/index/")
def index1():
    v = videos.Videos()
    data = v.getVideos(template=True)
    categories = v.getCategories()
    types = v.getTypes()
    return render_template('basic.html', videos = data, categories = categories, types=types)

@application.route('/download', methods=['POST'])
def download():
    videoname = request.form['video_name']
    return get_video(videoname)

########################################################################################################

@application.route("/videos/", methods=['GET'])
def get_videos():
    v = videos.Videos()
    return v.getVideos()

@application.route("/videos/load/<videoname>", methods=['GET'])
def get_video(videoname):
    v = videos.Videos()
    return v.getVideo(videoname)

@application.route("/videos/upload", methods=['POST'])
def add_video():
    v = videos.Videos()
    return v.addVideo()

@application.route("/events/")
def get_events():
    event = events.Events()
    return event.getEvents()

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
    image_files = request.files.getlist('image[]')
    imagename = request.form['image_name'] if request.form['image_name'] is not None else None
    category = request.form['image_category'] if request.form['image_category'] is not None else None

    return img.addImage(image_files,imagename,category=category)
    
# #################---------------------###################

@application.route("/audio/", methods=['GET'])
def get_audiofilenames():
    aud = audio.Audio()
    return aud.showAudioData()

@application.route('/audio/load/<audiofilename>', methods=['GET'])
def load_audio(audiofilename):
    aud = audio.Audio()
    return aud.loadAudio(audiofilename)

@application.route("/audio/upload", methods=['POST'])
def add_audio():
    aud = audio.Audio()
    return aud.addAudio()

# ##################-------------------------###################

# @app.route("/venues/")
# def get_venues():
#     venue = venues.Venues()
#     return venue.getVenues()

# ##################-------------------------###################


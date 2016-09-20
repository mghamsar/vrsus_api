from flask import Flask, request, redirect, render_template, jsonify
#from config import Config
#import flask.json
from app import images, events, videos
from app import application

@application.route("/")
@application.route("/index/")
def index1():
    v = videos.Videos()
    data = v.getVideos(template=True)
    #categories = v.getCategories()
    #types=v.getTypes()
    return render_template('basic.html')#, videos = data, categories = categories, types=types)

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
    v = videos.V
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

# ##################-------------------------###################

# @app.route("/venues/")
# def get_venues():
#     venue = venues.Venues()
#     return venue.getVenues()

# ##################-------------------------###################


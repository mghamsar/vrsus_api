from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

application = app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mghamsar:vrsus2016@vrsus.c7e2fotesw6y.us-east-1.rds.amazonaws.com/vrsus_dev'
db = SQLAlchemy(app)

from app import views, models
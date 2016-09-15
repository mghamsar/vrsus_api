from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import Config
import os

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mghamsar:vrsus2016@vrsus.c7e2fotesw6y.us-east-1.rds.amazonaws.com/vrsus'
db = SQLAlchemy(app)

from app import views, models
#!flask/bin/python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

# The WSGI configuration on Elastic Beanstalk requires
# the callable be named 'application' by default.

application = Flask(__name__)
application.config.from_object('config')
#application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mghamsar:vrsus2016@vrsus.c7e2fotesw6y.us-east-1.rds.amazonaws.com/vrsus_dev'
db = SQLAlchemy(application)

from app import views, models

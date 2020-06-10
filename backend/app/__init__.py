import random, string, json, os

from flask import Flask, render_template, request, redirect, jsonify, Response, url_for, flash, json

from flask_jwt_extended import JWTManager
from wtforms import SubmitField, StringField, RadioField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename

import configparser

from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from mongoengine.fields import BaseQuerySet

mongo_settings = configparser.ConfigParser()
mongo_settings.read('mongo-credentials.ini')

app = Flask(__name__)

# Return 500 error even if 
app.config['PROPAGATE_EXCEPTIONS'] = False

app.config['JWT_SECRET_KEY'] = 'another-incredibly-secret-phrase'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
# Don't expire access tokens
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

# WTForms configuration
app.config['WTF_CSRF_ENABLED'] = False
app.config['WTF_CSRF_CHECK_DEFAULT'] = False

# Mongodb configuration
app.config['MONGODB_SETTINGS'] = {
    'db' : mongo_settings[app.config['ENV']]['database'],
    'host': mongo_settings[app.config['ENV']]['hostname'],
}


# Change default json encoding to support ObjectID
from bson import ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app.json_encoder = JSONEncoder

jwt = JWTManager(app)

db = MongoEngine(app)

# Use MongoEngine to store session variables
app.session_interface = MongoEngineSessionInterface(db)

from app import mylogging

import tempfile

from app import import_scripts
from app.tasks import huey

import redis
r = redis.Redis(host="redis")

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

app.config['SECRET_KEY'] = 'bad-secret-keys-are-bad'
app.config['SERVER_NAME'] = os.environ.get('SERVER_NAME')

from app.routes import bp

app.register_blueprint(bp, url_prefix='/api')

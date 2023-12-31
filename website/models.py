from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#note model
class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(15000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    #foreignkey
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

#user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))
    notes = db.relationship('Note')
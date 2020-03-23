from datetime import datetime

from flask import current_app
from flaskapp import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'profile.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text(280), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    location = db.Colum(db.Text(40), nullable=True)
    image = db.Column(db.String(20), nullable=True)
    # likes = models.ManyToManyField(Profile,
    #    blank=True,
    #    through='Like',
    #    related_name='likes')

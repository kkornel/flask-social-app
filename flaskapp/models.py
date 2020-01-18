from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flaskapp import db

#  UserMixin, which provides default implementations for all of these properties and methods.
# is_authenticated
# is_active
# is_anonymous
# get_id()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(110), unique=True, nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
    # Passwords will be hashed and hash will have a length of 60 chars.
    password = db.Column(db.String(60), nullable=False)
    # Users have to have at least default img, so nullable=False.
    image = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"User({self.id}, '{self.email}', '{self.username}', '{self.password}', '{self.image}')"

    def __str__(self):
        # return f"User({self.id}, '{self.email}', '{self.image}')"
        return f"User({self.id}, '{self.email}', '{self.username}', '{self.password}', '{self.image}')"

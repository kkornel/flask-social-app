from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flaskapp import db, login_manager

# https://flask-login.readthedocs.io/en/latest/
# You will need to provide a user_loader callback.
# This callback is used to reload the user object from the user ID
# stored in the session. It should take the unicode ID of a user,
# and return the corresponding user object.
# For example:
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# It should return None (not raise an exception) if the ID is not valid.
# (In that case, the ID will manually be removed from the session
# and processing will continue.)


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

    def get_reset_password_token(self, expires_sec=1800):
        """This creates a token needed to reset password via email.
        Token is created using app's secret key. 
        He has expiration time. Default 30 mins.
        After that we need to generate new token.
        If token is valid (not expired) it returns:
            {'user_id': 1}
        Else:
            Exception: itsdangerous.exc.SignatureExpired: Signature expired
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # @staticmethod tells python not to except a self parameter as a argument
    @staticmethod
    def verify_reset_password_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User({self.id}, '{self.email}', '{self.username}', '{self.password}', '{self.image}')"

    def __str__(self):
        # return f"User({self.id}, '{self.email}', '{self.image}')"
        return f"User({self.id}, '{self.email}', '{self.username}', '{self.image}')"

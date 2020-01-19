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
    active = db.Column(db.Boolean, nullable=False, default=False)

    # def get_reset_password_token(self, expires_sec=1800):
    #     """This creates a token needed to reset password via email.
    #     Token is created using app's secret key.
    #     He has expiration time. Default 30 mins.
    #     After that we need to generate new token.
    #     If token is valid (not expired) it returns:
    #         {'user_id': 1}
    #     Else:
    #         Exception: itsdangerous.exc.SignatureExpired: Signature expired
    #     """
    #     s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'user_id': self.id}).decode('utf-8')

    # def get_activaction_token(self):
    #     """Almost the same as get_reset_password_token(), but
    #     expires_in is set to None
    #     """
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     return s.dumps({'user_id': self.id}).decode('utf-8')

    def get_token(self, expires_in, salt):
         """
        This creates a token needed to reset password via email.
        Token is created using app's secret key.
        He has expiration time. Default 30 mins.
        After that we need to generate new token.
        If token is valid (not expired) it returns:
            {'user_id': 1}
        Else:
            Exception: itsdangerous.exc.SignatureExpired: Signature expired
        """

        """
        Tha Salt

        https://pythonhosted.org/itsdangerous/

        All classes also accept a salt argument. The name might be misleading 
        because usually if you think of salts in cryptography 
        you would expect the salt to be something that is stored 
        alongside the resulting signed string as a way 
        to prevent rainbow table lookups. 
        Such salts are usually public.

        In “itsdangerous”, like in the original Django implementation, 
        the salt serves a different purpose. 
        You could describe it as namespacing. 
        It’s still not critical if you disclose 
        it because without the secret key it does not help an attacker.

        Let’s assume that you have two links you want to sign. 
        You have the activation link on your system 
        which can activate a user account and then 
        you have an upgrade link that can upgrade 
        a user’s account to a paid account which you send out via email. 
        If in both cases all you sign is the user ID a user could reuse 
        the variable part in the URL from the activation link 
        to upgrade the account.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_in)
        current_app.logger.info('Serializer: %s', s)
        return s.dumps({'user_id': self.id}, salt=salt).decode('utf-8')

    # @staticmethod tells python not to except a self parameter as a argument
    # @staticmethod
    # def verify_reset_password_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     return User.query.get(user_id)

    # @staticmethod tells python not to except a self parameter as a argument
    @staticmethod
    def verify_token(token, salt):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt=salt)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User({self.id}, '{self.email}', '{self.username}', '{self.password}', '{self.image}')"

    def __str__(self):
        # return f"User({self.id}, '{self.email}', '{self.image}')"
        return f"User({self.id}, '{self.email}', '{self.username}', '{self.image}')"

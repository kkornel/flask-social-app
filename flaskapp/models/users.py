from datetime import datetime

from flask import current_app as app
from flask import current_app
from flask import url_for, render_template

from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import event

from flaskapp import db, login_manager, bcrypt
from flaskapp.utils import delete_image, save_image
from flaskapp.users.utils import send_email
from flaskapp.models.social import Post

from sqlalchemy import or_


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

# UserMixin, which provides default implementations for all of these properties and methods.
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
    active = db.Column(db.Boolean, nullable=False, default=False)
    # Post attribute has a relationship to the Post model.
    # Backref is simillar to adding another column to the Post model.
    # When we have a Post we can use author attribute to get the user who created the post.
    # lazy - defines when SQLAlchemy loads the data from the database.
    # lazy=True - means that SQLAlchemy will load the data as necessary in one go.
    # Post is with capital letter because it is referencing the actual class.
    profile = db.relationship('Profile',
                              uselist=False,
                              cascade="all, delete-orphan",
                              passive_deletes=True,
                              backref='user')
    date_joined = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)

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

    def send_verification_email(self):
        token = self.get_token(
            None, current_app.config['SECURITY_VERIFY_EMAIL_SALT'])
        confirm_url = url_for('users.confirm_email',
                              token=token,
                              _external=True)
        html = render_template('users/mail_verify_email.html',
                               confirm_url=confirm_url)
        subject = 'Please confirm your email'
        send_email(self.email, subject, html)

    def send_reset_password_email(self):
        token = self.get_token(
            3600, current_app.config['SECURITY_RESET_PASSWORD_SALT'])
        reset_url = url_for('users.reset_password_token',
                            token=token,
                            _external=True)
        html = render_template('users/mail_reset_password.html',
                               reset_url=reset_url)
        subject = 'Password Reset Request'
        send_email(self.email, subject, html)

    def verify_password(self, password_to_verify):
        return bcrypt.check_password_hash(self.password, password_to_verify)

    def __repr__(self):
        return f"User({self.id}, '{self.email}', '{self.username}', '{self.password}')"

    def __str__(self):
        return f"User(#{self.id},  '{self.username}')"


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('profile.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('profile.id')),
)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id', ondelete='CASCADE'),
                        nullable=False)
    bio = db.Column(db.String(300), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(40), nullable=True)
    # Users have to have at least default img, so nullable=False.
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post',
                            cascade="all, delete-orphan",
                            backref='author')
    comments = db.relationship('Comment',
                               cascade="all, delete-orphan",
                               backref='author')
    '''
    * Profile is the right side entity of the relationship (the left side entity is the parent class). 
    Since this is a self-referential relationship, I have to use the same class on both sides.

    * secondary configures the association table that is used for this relationship, 
    which I defined right above this class.

    * primaryjoin indicates the condition that links the left side entity (the follower user) with the association table. 
    The join condition for the left side of the relationship is the user ID matching the follower_id field of the association table. 
    The followers.c.follower_id expression references the follower_id column of the association table.

    * secondaryjoin indicates the condition that links the right side entity (the followed user) with the association table. 
    This condition is similar to the one for primaryjoin, with the only difference that now I'm using followed_id, 
    which is the other foreign key in the association table.

    * backref defines how this relationship will be accessed from the right side entity. 
    From the left side, the relationship is named followed, so from the right side I am going to use the name followers 
    to represent all the left side users that are linked to the target user in the right side. 
    The additional lazy argument indicates the execution mode for this query. 
    A mode of dynamic sets up the query to not run until specifically requested, which is also how I set up the posts one-to-many relationship.

    * lazy is similar to the parameter of the same name in the backref, but this one applies to the left side query instead of the right side.'
    '''
    followed = db.relationship('Profile',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def add_image(self, image_data):
        picture_file_name = save_image(
            image_data, app.config['UPLOAD_FOLDER_PROFILE_IMGS'], (125, 125))
        self.image = picture_file_name

    def delete_image(self):
        if self.image != 'default.jpg':
            delete_image(app.config['UPLOAD_FOLDER_PROFILE_IMGS'], self.image)
            self.image = 'default.jpg'

    def set_default_image(self):
        self.delete_image()
        self.image = 'default.jpg'

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            self.followed_posts()

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def is_followed_by(self, user):
        return self.followers.filter(
            followers.c.follower_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.author_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.date_posted.desc()).all()

    def user_and_followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.author_id)).filter(
                or_(followers.c.follower_id == self.id,
                    Post.author_id == self.id)).order_by(
                        Post.date_posted.desc()).all()

    def __str__(self):
        return f"Profile(#{self.id} of {self.user})"


# standard decorator style
@event.listens_for(User, 'before_delete')
def receive_before_delete(mapper, connection, target):
    "listen for the 'before_delete' event"
    app.logger.debug('User before_delete')
    # ... (event handling logic) ...


@event.listens_for(Profile, 'before_delete')
def receive_before_delete(mapper, connection, target):
    "listen for the 'before_delete' event"
    app.logger.debug('Profile before_delete')
    # ... (event handling logic) ...

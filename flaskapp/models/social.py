from datetime import datetime

from flask import current_app as app
from flaskapp import db

from flaskapp.utils import delete_image, save_image

likes = db.Table(
    'likes',
    db.Column('profile_id',
              db.Integer,
              db.ForeignKey('profile.id'),
              primary_key=True),
    db.Column('post_id',
              db.Integer,
              db.ForeignKey('post.id'),
              primary_key=True),
    db.Column('date_liked',
              db.DateTime,
              nullable=False,
              default=datetime.utcnow),
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer,
                          db.ForeignKey('profile.id', ondelete='CASCADE'),
                          nullable=False)
    content = db.Column(db.String(280), nullable=False)
    location = db.Column(db.String(40), nullable=True)
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)
    image = db.Column(db.String(20), nullable=True)
    comments = db.relationship('Comment',
                               cascade="all, delete-orphan",
                               backref='post')
    likes = db.relationship('Profile',
                            secondary=likes,
                            lazy='subquery',
                            backref=db.backref('likes', lazy=True))

    def add_image(self, image_data):
        picture_file_name = save_image(image_data,
                                       app.config['UPLOAD_FOLDER_POSTS_IMGS'],
                                       (510, 515))
        self.image = picture_file_name

    def delete_image(self):
        if self.image:
            delete_image(app.config['UPLOAD_FOLDER_POSTS_IMGS'], self.image)
            self.image = None

    def __repr__(self):
        return f"Post({self.id}, '{self.author_id}', '{self.content}', '{self.location}', '{self.date_posted}', '{self.image}')"

    def __str__(self):
        return f"Post(#{self.id})"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer,
                        db.ForeignKey('post.id', ondelete='CASCADE'),
                        nullable=False)
    author_id = db.Column(db.Integer,
                          db.ForeignKey('profile.id', ondelete='CASCADE'),
                          nullable=False)
    content = db.Column(db.String(280), nullable=False)
    date_commented = db.Column(db.DateTime,
                               nullable=False,
                               default=datetime.utcnow)

    def __repr__(self):
        return f"Comment({self.id}, '{self.post_id}', '{self.author_id}', '{self.content}', '{self.date_commented}')"

    def __str__(self):
        return f"Comment(#{self.id} of {self.post})"

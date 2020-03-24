from datetime import datetime

from flask import current_app
from flaskapp import db


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

    # likes = models.ManyToManyField(Profile,
    #    blank=True,
    #    through='Like',
    #    related_name='likes')

    def __repr__(self):
        return f"Post({self.id}, '{self.author_id}', '{self.content}', '{self.location}', '{self.date_posted}', '{self.image}')"

    def __str__(self):
        return f"Post({self.id}, '{self.author}', '{self.content}')"


# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     post_id = db.Column(db.Integer,
#                         db.ForeignKey('post.id', ondelete='CASCAE'),
#                         nullable=False)
#     author_id = db.Column(db.Integer,
#                           db.ForeignKey('profile.id', ondelete='CASCAE'),
#                           nullable=False)
#     content = db.Column(db.String(280), nullable=False)
#     date_commented = db.Column(db.DateTime,
#                                nullable=False,
#                                default=datetime.utcnow)

#     def __repr__(self):
#         return f"Comment({self.id}, '{self.post_id}', '{self.author_id}', '{self.content}', '{self.date_commented}')"

#     def __str__(self):
#         return f"Comment({self.id}, '{self.post}', '{self.author}', '{self.content})"

# class Like(db.Model):

from flaskapp import ma

from flaskapp.models.users import User, Profile
from flaskapp.models.social import Post, Comment


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    email = ma.auto_field()
    username = ma.auto_field()
    profile_id = ma.auto_field('profile')
    date_joined = ma.auto_field()


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        include_fk = True

    user = ma.Nested(UserSchema, only=('username', ))
    posts = ma.auto_field()
    comments = ma.auto_field()
    followed = ma.auto_field()
    followers = ma.auto_field()


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True

    comments = ma.auto_field()
    likes = ma.auto_field()


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        include_fk = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
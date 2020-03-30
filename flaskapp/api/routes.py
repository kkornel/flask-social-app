from flask import Blueprint, current_app as app, jsonify, abort
from flask_restful import Api

from flaskapp.models.users import User, Profile
from flaskapp.models.social import Post, Comment
from flaskapp.api.schemas import (user_schema, users_schema, profile_schema,
                                  profiles_schema, post_schema, posts_schema,
                                  comment_schema, comments_schema)
from flaskapp.api.resources import (UsersResource, UserResource,
                                    ProfilesResource, ProfileResource,
                                    PostsResource, PostResource,
                                    CommentsResource, CommentResource)
api_bp = Blueprint('api', __name__)

# Using Resources from flask_restful
api = Api(api_bp)

api.add_resource(UsersResource, '/api/resources/users')
api.add_resource(UserResource, '/api/resources/user/<int:id>/')
api.add_resource(ProfilesResource, '/api/resources/profiles/')
api.add_resource(ProfileResource, '/api/resources/profile/<string:username>/')
api.add_resource(PostsResource, '/api/resources/posts/')
api.add_resource(PostResource, '/api/resources/post/<int:id>/')
api.add_resource(CommentsResource, '/api/resources/comments/')
api.add_resource(CommentResource, '/api/resources/comment/<int:id>/')


# Using standard routes and blueprint
@api_bp.route("/api/users/")
def users():
    all_users = User.query.all()
    return jsonify(users_schema.dump(all_users))


@api_bp.route("/api/user/<int:id>/")
def user_detail(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error_code': '404', 'message': 'User not found.'})
    return user_schema.dump(user)


@api_bp.route("/api/profiles/")
def profiles():
    all_profiles = Profile.query.all()
    return jsonify(profiles_schema.dump(all_profiles))


@api_bp.route("/api/profile/<string:username>/")
def profile_detail(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error_code': '404', 'message': 'Profile not found.'})
    return profile_schema.dump(user.profile)


@api_bp.route("/api/posts/")
def posts():
    all_posts = Post.query.all()
    return jsonify(posts_schema.dump(all_posts))


@api_bp.route("/api/post/<int:id>/")
def post_detail(id):
    post = Post.query.get(id)
    if not post:
        return jsonify({'error_code': '404', 'message': 'Post not found.'})
    return post_schema.dump(post)


@api_bp.route("/api/comments/")
def comments():
    all_comments = Comment.query.all()
    return jsonify(comments_schema.dump(all_comments))


@api_bp.route("/api/comment/<int:id>/")
def comment_detail(id):
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({'error_code': '404', 'message': 'Comment not found.'})
    return comment_schema.dump(comment)
from flask_restful import Resource

from flaskapp.models.users import User, Profile
from flaskapp.models.social import Post, Comment

from flaskapp.api.schemas import (user_schema, users_schema, profile_schema,
                                  profiles_schema, post_schema, posts_schema,
                                  comment_schema, comments_schema)


class UsersResource(Resource):
    def get(self):
        all_users = User.query.all()
        return {'status': 'success', 'data': users_schema.dump(all_users)}, 200


class UserResource(Resource):
    def get(self, id):
        user = User.query.get(id)
        if not user:
            return {'status': 'error', 'data': 'User not found.'}, 404
        return {'status': 'success', 'data': user_schema.dump(user)}, 200


class ProfilesResource(Resource):
    def get(self):
        all_profiles = Profile.query.all()
        return {
            'status': 'success',
            'data': profiles_schema.dump(all_profiles)
        }, 200


class ProfileResource(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'status': 'error', 'data': 'Profile not found.'}, 404
        return {
            'status': 'success',
            'data': profile_schema.dump(user.profile)
        }, 200


class PostsResource(Resource):
    def get(self):
        all_posts = Post.query.all()
        return {'status': 'success', 'data': posts_schema.dump(all_posts)}, 200


class PostResource(Resource):
    def get(self, id):
        post = Post.query.get(id)
        if not post:
            return {'status': 'error', 'data': 'Post not found.'}, 404
        return {'status': 'success', 'data': post_schema.dump(post)}, 200

    # def post(self):
    #     json_data = request.get_json(force=True)
    #     if not json_data:
    #         return {'message': 'No input data provided'}, 400
    #     # Validate and deserialize input
    #     data, errors = category_schema.load(json_data)
    #     if errors:
    #         return errors, 422
    #     category = Category.query.filter_by(name=data['name']).first()
    #     if category:
    #         return {'message': 'Category already exists'}, 400
    #     category = Category(name=json_data['name'])

    #     db.session.add(category)
    #     db.session.commit()

    #     result = category_schema.dump(category).data

    #     return {"status": 'success', 'data': result}, 201

    # def put(self):
    #     json_data = request.get_json(force=True)
    #     if not json_data:
    #         return {'message': 'No input data provided'}, 400
    #     # Validate and deserialize input
    #     data, errors = category_schema.load(json_data)
    #     if errors:
    #         return errors, 422
    #     category = Category.query.filter_by(id=data['id']).first()
    #     if not category:
    #         return {'message': 'Category does not exist'}, 400
    #     category.name = data['name']
    #     db.session.commit()

    #     result = category_schema.dump(category).data

    #     return {"status": 'success', 'data': result}, 204

    # def delete(self):
    #     json_data = request.get_json(force=True)
    #     if not json_data:
    #         return {'message': 'No input data provided'}, 400
    #     # Validate and deserialize input
    #     data, errors = category_schema.load(json_data)
    #     if errors:
    #         return errors, 422
    #     category = Category.query.filter_by(id=data['id']).delete()
    #     db.session.commit()

    #     result = category_schema.dump(category).data

    #     return {"status": 'success', 'data': result}, 204


class CommentsResource(Resource):
    def get(self):
        all_comments = Comment.query.all()
        return {
            'status': 'success',
            'data': comments_schema.dump(all_comments)
        }, 200


class CommentResource(Resource):
    def get(self, id):
        comment = Comment.query.get(id)
        if not comment:
            return {'status': 'error', 'data': 'Comment not found.'}, 404
        return {'status': 'success', 'data': comment_schema.dump(comment)}, 200
from functools import wraps

from flask import abort, redirect, url_for, request, current_app as app, session

from flask_login import current_user

from flaskapp.models.social import Post
from flaskapp.models.users import User


def is_author(view_func):
    @wraps(view_func)
    def _wrapped_view(post_id, *args, **kwargs):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user.profile:
            abort(403)
        return view_func(post_id, *args, **kwargs)

    return _wrapped_view


def is_owner_of_the_account(view_func):
    @wraps(view_func)
    def _wrapped_view(username, *args, **kwargs):
        user = User.query.filter_by(username=username).first()
        if user != current_user:
            abort(403)
        return view_func(username, *args, **kwargs)

    return _wrapped_view


def prevent_authenticated(view_func):
    """
    Custom decorator for preventing logged users from visitng sites
    which are intendent for anonymous users.
    """
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        return view_func(*args, **kwargs)

    return _wrapped_view


# def confirm_password(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         last_login = request.user.last_login
#         timespan = last_login + datetime.timedelta(seconds=10)
#         if timezone.now() > timespan:
#             from .views import PasswordConfirmView
#             return PasswordConfirmView.as_view()(request, *args, **kwargs)
#         return view_func(request, *args, **kwargs)

#     return _wrapped_view

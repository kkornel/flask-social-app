import datetime
import re

from flask import Blueprint, render_template, request, make_response, current_app as app, Markup

from flask_login import current_user

from flaskapp.utils import generate_hashtag_link, generate_link
from flaskapp.models.social import Post, Comment
from flaskapp.models.users import Profile

main = Blueprint('main', __name__)

# We will not be using global app variable here in @app.route
# to creates routes anymore.
# Instead we are going to create route specifically for this user's blueprint.
# And then register these with the application later.

# To the function href="{{ url_for('users.login') }} we are passing the name of the function, not the route.


# This is decorator. Additional fuctionality to exisitng functions.
# app.route will handle all of the complicated backend stuff and simply allow us to write a function that returns information that will be shown on our website for this specific route.
@main.route('/')
@main.route('/home/')
def home():
    response = make_response(
        render_template('home.html', title='Master Thesis Flask'))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    # return response
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('home.html',
                           title='Master Thesis Flask',
                           posts=posts)


@main.app_template_filter('render_tags_and_links')
def _render_tags_and_links(obj):
    if obj == None:
        return ''
    text = re.sub(r"#(\w+)", lambda m: generate_hashtag_link(m.group(1)), obj)
    # return re.sub(r"(?P<url>https?://[^\s]+)", lambda m: generate_link(m.group(1)), text)

    # If you want Django to mark it as safe content, you can do the following:
    # return mark_safe(
    #     re.sub(
    #         r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*",
    #         lambda m: generate_link(m.group(0)), text))
    return Markup(
        re.sub(
            r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*",
            lambda m: generate_link(m.group(0)), text))


@main.app_template_filter('render_links')
def _render_links(obj):
    return Markup(
        re.sub(
            r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*",
            lambda m: generate_link(m.group(0)), obj))


@main.app_template_filter('time_since_date_posted')
def _time_since_date_posted(obj):
    if obj is not None:
        diff = datetime.datetime.utcnow() - obj
        s = diff.seconds
        if diff.days > 30 or diff.days < 0:
            return obj.strftime('Y-m-d H:i')
        elif diff.days == 1:
            return 'One day ago'
        elif diff.days > 1:
            return '{} days ago'.format(diff.days)
        elif s <= 1:
            return 'just now'
        elif s < 60:
            return '{} seconds ago'.format(s)
        elif s < 120:
            return 'one minute ago'
        elif s < 3600:
            return '{} minutes ago'.format(round(s / 60))
        elif s < 7200:
            return 'one hour ago'
        else:
            return '{} hours ago'.format(round(s / 3600))
    else:
        return None


@main.app_context_processor
def utility_processor():
    def has_user_commented(post_id):
        try:
            profile = current_user.profile
            post = Post.query.get(post_id)
            all_user_comments_for_that_post = Comment.query.filter_by(
                post_id=post_id, author_id=profile.id).all()
            has_commented = len(all_user_comments_for_that_post) > 0
            return has_commented
        except Exception as e:
            print(e)
            return False

    def is_already_following(follower_id, following_id):
        app.logger.debug(f'FILTERS: {follower_id} {following_id}')

        try:
            follower = Profile.query.get(follower_id)
            following = Profile.query.get(following_id)
            # is_following = follower.is_following(following)
            # app.logger.debug(f'FILTERS: {is_following}')
            # return is_following
            return False
        except Exception:
            return False

    return dict(has_user_commented=has_user_commented,
                is_already_following=is_already_following)

import re

from flask import Blueprint, current_app as app, redirect, render_template, request, url_for, request
from flask.views import View

from flask_login import current_user, login_required

from flaskapp import db
from flaskapp.decorators import is_author, prevent_authenticated
from flaskapp.utils import generate_hashtag_link, generate_link, save_image, delete_image
from flaskapp.social.forms import PostCreateForm, PostDeleteForm, PostUpdateForm
from flaskapp.models.social import Post

social = Blueprint('social', __name__)


@social.route('/new', methods=['GET', 'POST'])
@login_required
def post_create():
    form = PostCreateForm()
    if form.validate_on_submit():
        author = current_user.profile
        post = Post(author_id=author.id,
                    content=form.content.data,
                    location=form.location.data,
                    image=form.image.data)

        db.session.add(post)
        db.session.commit()

        app.logger.debug(current_user)
        app.logger.debug(current_user.profile)
        app.logger.debug(current_user.profile.posts)
        app.logger.debug(post)
        app.logger.debug(form.content.data)
        app.logger.debug(form.location.data)
        app.logger.debug(form.image.data)

        post = Post.query.filter_by(author=author).first()
        app.logger.debug(post)
        return redirect(url_for('social.post_detail', post_id=post.id))
    return render_template('social/post_create.html',
                           title='Create post',
                           form=form)


@social.route('/post/<int:post_id>/', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('social/post_detail.html', post=post)


@social.route('/post/<int:post_id>/update/', methods=['GET', 'POST'])
@login_required
@is_author
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostUpdateForm()
    if form.validate_on_submit():
        post.content = form.content.data
        post.location = form.location.data
        print(post.image)
        print(form.delete_current_image.data)
        delete_image('static\posts_imgs', post.image)
        print(post.image)
        if form.delete_current_image.data:
            if post.image:
                print()
        if form.image.data:
            picture_file_name = save_image(form.image.data,
                                           'static/posts_imgs', (510, 515))
            post.image = picture_file_name
        db.session.commit()
        return redirect(url_for('social.post_detail', post_id=post.id))
    if request.method == 'GET':
        form.content.data = post.content
        form.location.data = post.location
        form.image.data = post.image
    return render_template('social/post_update.html', form=form)


@social.route('/post/<int:post_id>/delete/', methods=['GET', 'POST'])
@is_author
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostDeleteForm()
    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('social/post_confirm_delete.html',
                           form=form,
                           post=post)


class MyView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = PostCreateForm()

        if request.method == 'POST':
            app.logger.debug('valid')

            if form.validate_on_submit():
                app.logger.debug('valid')
        return render_template('social/post_create.html',
                               title='Create post',
                               form=form)


# with app.app_context():
#     app.add_url_rule('/new2', view_func=MyView.as_view('myview'))


@social.app_template_filter('render_tags_and_links')
def _render_tags_and_links(obj):
    text = re.sub(r"#(\w+)", lambda m: generate_hashtag_link(m.group(1)), obj)
    # return re.sub(r"(?P<url>https?://[^\s]+)", lambda m: generate_link(m.group(1)), text)

    # If you want Django to mark it as safe content, you can do the following:
    # return mark_safe(
    #     re.sub(
    #         r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*",
    #         lambda m: generate_link(m.group(0)), text))
    return re.sub(
        r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*",
        lambda m: generate_link(m.group(0)), text)

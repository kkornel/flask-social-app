import re

from flask import Blueprint, current_app as app, redirect, render_template, request, url_for, request
from flask.views import View

from flask_login import current_user, login_required

from flaskapp import db
from flaskapp.decorators import is_author, prevent_authenticated
from flaskapp.utils import save_image, delete_image
from flaskapp.social.forms import PostCreateForm, PostDeleteForm, PostUpdateForm
from flaskapp.models.social import Post

social = Blueprint('social', __name__)


@social.route('/new/To', methods=['GET', 'POST'])
@login_required
def post_create():
    form = PostCreateForm()
    if form.validate_on_submit():
        author = current_user.profile
        post = Post(author_id=author.id,
                    content=form.content.data,
                    location=form.location.data)
        if form.image.data:
            post.add_image(form.image.data)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('social.post_detail', post_id=post.id))
    return render_template('social/post_create.html',
                           title='Create post',
                           form=form)


@social.route('/post/<int:post_id>/', methods=['GET', 'POST'])
@login_required
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
        if form.delete_current_image.data:
            if post.image:
                post.delete_image()
        if form.image.data:
            if post.image:
                post.delete_image()
            post.add_image(form.image.data)
        db.session.commit()
        return redirect(url_for('social.post_detail', post_id=post.id))
    if request.method == 'GET':
        form.content.data = post.content
        form.location.data = post.location
        form.image.data = post.image
    return render_template('social/post_update.html', form=form)


@social.route('/post/<int:post_id>/delete/', methods=['GET', 'POST'])
@login_required
@is_author
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostDeleteForm()
    if form.validate_on_submit():
        if post.image:
            post.delete_image()
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


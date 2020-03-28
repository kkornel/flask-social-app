import re

from flask import Blueprint, current_app as app, redirect, render_template, request, url_for, request, jsonify
from flask.views import View

from flask_login import current_user, login_required

from flaskapp import db
from flaskapp.decorators import is_author, prevent_authenticated
from flaskapp.utils import save_image, delete_image
from flaskapp.social.forms import PostCreateForm, PostDeleteForm, PostUpdateForm, CommentCreateForm, CommentDeleteForm
from flaskapp.models.social import Post, Comment
from flaskapp.models.users import User, Profile

social = Blueprint('social', __name__)


@social.route('/like/', methods=['POST'])
def like():
    if request.method == 'POST':
        post_id = request.form['post_id']
        profile_id = request.form['profile_id']

        profile = Profile.query.get(profile_id)
        post = Post.query.get(post_id)

        if profile in post.likes:
            post.likes.remove(profile)
        else:
            post.likes.append(profile)

        db.session.add(post)
        db.session.commit()

        return jsonify({'likes_count': len(post.likes)})
    return jsonify({'error': 'GET method'})


@social.route('/follow/', methods=['POST'])
def follow():
    if request.method == 'POST':
        follower_id = request.form['follower_id']
        followed_id = request.form['followed_id']

        follower = Profile.query.get(follower_id)
        followed = Profile.query.get(followed_id)

        if follower.is_following(followed):
            follower.unfollow(followed)
        else:
            follower.follow(followed)

        db.session.commit()

        return jsonify({
            'followers': followed.followers.count(),
            'following': followed.followed.count()
        })
    return jsonify({'error': 'GET method'})


@social.route('/new/', methods=['GET', 'POST'])
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
    form = CommentCreateForm()
    if form.validate_on_submit():
        comment = Comment(post_id=post_id,
                          author_id=current_user.profile.id,
                          content=form.content.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('social.post_detail', post_id=post.id))
    return render_template('social/post_detail.html', post=post, form=form)


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


@social.route('/post/<int:post_id>/comment/<int:comment_id>/delete/',
              methods=['GET', 'POST'])
def comment_delete(post_id, comment_id):
    post = Post.query.get_or_404(post_id)
    comment = Comment.query.get_or_404(comment_id)
    form = CommentDeleteForm()
    if form.validate_on_submit():
        db.session.delete(comment)
        db.session.commit()
        form = CommentCreateForm()
        return redirect(
            url_for('social.post_detail', form=form, post_id=post_id))
    return render_template('social/comment_confirm_delete.html',
                           form=form,
                           comment=comment)


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
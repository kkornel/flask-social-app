from flask import Blueprint, current_app as app, redirect, render_template, request, url_for
from flask.views import View

from flask_login import current_user, login_required

from flaskapp import db
from flaskapp.social.forms import PostCreateForm
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


@social.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('social/post_detail.html', post=post)

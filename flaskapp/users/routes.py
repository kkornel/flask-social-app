from flask import current_app as app
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_user, logout_user, login_required

from flaskapp import db, bcrypt
from flaskapp.users.forms import (LoginForm, RegistrationForm,
                                  RequestPasswordResetForm, ResetPasswordForm,
                                  UpdateProfileForm, ProfileUpdateForm,
                                  ChangeEmailForm, ChangePasswordForm,
                                  PasswordVerifyForm, ProfileDeleteForm)

from flaskapp.decorators import prevent_authenticated, is_owner_of_the_account
from flaskapp.models.users import User, Profile

users = Blueprint('users', __name__)

# We will not be using global app variable here in @app.route
# to creates routes anymore.
# Instead we are going to create route specifically for this user's blueprint.
# And then register these with the application later.


@users.route('/register/', methods=['GET', 'POST'])
@prevent_authenticated
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # bcrypt.generate_password_hash(form.password.data) - returns bytes
        # bcrypt.generate_password_hash(form.password.data).decode('utf-8') - returns string
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        user = User(email=form.email.data,
                    username=form.username.data,
                    password=hashed_password)
        # TODO delete
        user.active = True

        db.session.add(user)
        db.session.commit()

        profile = Profile(user_id=user.id, user=user)
        db.session.add(profile)
        db.session.commit()

        user.send_verification_email()
        # 'success' is the name of the BootStrap class for message.
        flash(f'A confirmation email has been sent to {form.email.data}',
              'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)


@users.route('/confirm/<token>/')
def confirm_email(token):
    user = User.verify_token(token,
                             current_app.config['SECURITY_VERIFY_EMAIL_SALT'])
    if user is None:
        flash('That is an invalid or expired token', 'warning')
    elif user.active:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.active = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. You can log in now.',
              'success')
    return redirect(url_for('users.login'))


@users.route('/login/', methods=['GET', 'POST'])
@prevent_authenticated
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            if not user.active:
                flash('In order to log in please confirm your account!',
                      'warning')
                return render_template('users/login.html',
                                       title='Login',
                                       form=form)
            # remember refers to the Remember me on Login page.
            login_user(user, remember=form.remember.data)
            # When we try to access a page that requires login, eg. account page.
            # It redirects us to login page, and in the URL there is parameter of the page
            # that we wanted to visit:
            # http://127.0.0.1:5000/login?next=%2Faccount
            # Here we are getting that parameter and redirecting user to that page.
            next_page = request.args.get('next')
            # current_app.logger.info('Next page parameter: %s', next_page)
            return redirect(next_page) if next_page else redirect(
                url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password.',
                  'danger')
    return render_template('users/login.html', title='Login', form=form)


@users.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route('/reset_password/', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        user.send_reset_password_email()
        flash(
            'An email has been sent with instructions to reset your password.',
            'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_password_request.html',
                           title='Reset Password',
                           form=form)


@users.route('/reset_password/<token>/', methods=['GET', 'POST'])
def reset_password_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_token(
        token, current_app.config['SECURITY_RESET_PASSWORD_SALT'])
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.',
              'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset_password_token.html',
                           title='Set New Password',
                           form=form)


@users.route('/<string:username>/', methods=['GET'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    profile = User.query.filter_by(username=username).all()[0].profile
    return render_template('users/profile.html',
                           title=username,
                           profile=profile,
                           posts=profile.posts)


@users.route('/<string:username>/delete/', methods=['GET', 'POST'])
@login_required
@is_owner_of_the_account
def delete_account(username):
    form = PasswordVerifyForm()
    if form.validate_on_submit():
        return redirect(
            url_for('users.delete_account_confirmation', username=username))
    return render_template('users/profile_password_verify.html',
                           title='Verify password',
                           form=form)


@users.route('/<string:username>/delete-confirmation/',
             methods=['GET', 'POST'])
@login_required
@is_owner_of_the_account
def delete_account_confirmation(username):
    form = ProfileDeleteForm()
    if form.validate_on_submit():
        db.session.delete(current_user.profile)
        db.session.delete(current_user)
        db.session.commit()
        flash('Your account has been deleted', 'danger')
        return redirect(url_for('users.login'))
    return render_template('users/profile_delete_confirm.html',
                           title='Account deletion',
                           form=form)


@users.route('/<string:username>/password-change/', methods=['GET', 'POST'])
@login_required
@is_owner_of_the_account
def password_change(username):
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(
            url_for('users.profile', username=current_user.username))
    return render_template('users/profile_password_change.html',
                           title='Change password',
                           form=form)


@users.route('/<string:username>/email-update/', methods=['GET', 'POST'])
@login_required
@is_owner_of_the_account
def email_update(username):
    form = ChangeEmailForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(
            url_for('users.profile', username=current_user.username))
    elif request.method == 'GET':
        form.email.data = current_user.email
    return render_template('users/profile_email_update.html',
                           title='Update email',
                           form=form)


@users.route('/<string:username>/update/', methods=['GET', 'POST'])
@login_required
@is_owner_of_the_account
def edit_profile(username):
    form = ProfileUpdateForm()
    if form.validate_on_submit():
        if form.image.data:
            if current_user.profile.image:
                current_user.profile.delete_image()
            current_user.profile.add_image(form.image.data)
        if form.delete_current_image.data:
            current_user.profile.set_default_image()
        current_user.username = form.username.data
        current_user.profile.bio = form.bio.data
        current_user.profile.city = form.city.data
        current_user.profile.website = form.website.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(
            url_for('users.profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.bio.data = current_user.profile.bio
        form.city.data = current_user.profile.city
        form.website.data = current_user.profile.website
    return render_template('users/profile_update.html',
                           title='Update profile',
                           form=form)


# Code for commented section in 'users/profile_update.html'
# All fields (email, username, password, bio, ..., in one page)
# @users.route('/<string:username>/update/', methods=['GET', 'POST'])
# @login_required
# @is_owner_of_the_account
# def edit_profile(username):
#     form = UpdateProfileForm()
#     if form.validate_on_submit():
#         # We have to check because this field is not required.
#         if form.image.data:
#             if current_user.profile.image:
#                 current_user.profile.delete_image()
#             current_user.profile.add_image(form.image.data)
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         if form.password.data:
#             hashed_password = bcrypt.generate_password_hash(
#                 form.password.data).decode('utf-8')
#             current_user.password = hashed_password
#         current_user.profile.bio = form.bio.data
#         current_user.profile.city = form.city.data
#         current_user.profile.website = form.website.data
#         db.session.commit()
#         flash('Your account has been updated!', 'success')
#         # You want to use redirect here instead of fall down to render_template
#         # and the reason is of something called Post-Get-Redirect-Pattern
#         # If you ever reloaded a form after submiting a data
#         # and then a weird message comes "Are you sure you wanna reload?
#         # Because the data will be resubmited."
#         # That is because the browser is telling you that
#         # you about to run another POST request when you reload your page.
#         # So redirecting is causing to send a GET request
#         # and then we dont get that weird message.
#         return redirect(
#             url_for('users.profile', username=current_user.username))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#         form.bio.data = current_user.profile.bio
#         form.city.data = current_user.profile.city
#         form.website.data = current_user.profile.website
#     return render_template('users/profile_update.html',
#                            title='Update profile',
#                            form=form)

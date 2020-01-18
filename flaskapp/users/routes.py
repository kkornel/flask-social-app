from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required

from flaskapp import db, bcrypt
from flaskapp.models import User
from flaskapp.users.forms import LoginForm, RegistrationForm

users = Blueprint('users', __name__)

# We will not be using global app variable here in @app.route
# to creates routes anymore.
# Instead we are going to create route specifically for this user's blueprint.
# And then register these with the application later.


@users.route('/register', methods=['GET', 'POST'])
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
                    username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        current_app.logger.info('%s logged in successfully', user)
        # 'success' is the name of the BootStrap class for message.
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


@users.route('/')
def reset_request():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

from flask import Blueprint, flash, redirect, render_template, request

from flaskapp import db
from flaskapp.models import User
from flaskapp.users.forms import LoginForm, RegistrationForm

users = Blueprint('users', __name__)

# We will not be using global app variable here in @app.route
# to creates routes anymore.
# Instead we are going to create route specifically for this user's blueprint.
# And then register these with the application later.


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


@users.route('/')
def reset_request():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

import logging

from flask import Flask

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

from flaskapp.config import Config

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format':
            '[%(levelname)s] [%(asctime)s] [%(name)s.%(funcName)s] ->  %(message)s',
            'datefmt': '%H:%M:%S',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default',
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

# __name__ - name of the module
# If we run this, this will be equal __main__
# For Flask to know where to look for static files and templates etc.
# app = Flask(__name__)

# After moving config to config.py
# app.config.from_object(Config)

# >>> import secrets
# >>> secrets.token_hex(16)
# app.config['SECRET_KEY'] = '046e22b94eeaa82d1a6d721f0da941ec'

# '///' is relavitve path to current file.
# So site.db will be created where flaskblog.py is located.
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# After using config_class we are removing (app) from extensions and
# using .init_app(app) in create_app()
db = SQLAlchemy()
# db = SQLAlchemy(app)

bcrypt = Bcrypt()
# bcrypt = Bcrypt(app)

login_manager = LoginManager()
# login_manager = LoginManager(app)

mail = Mail()
# mail = Mail(app)

# It tells the login_manager where is login route.
# @login_required needs to know where to redirect user
# if he is not logged in.
login_manager.login_view = 'users.login'

# Styling the flash message for @login_required that pops up on login page.
login_manager.login_message_category = 'info'

# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

# It needs to be here, becuase in routes.py we are importing app and
# if that import below would be at the top, the app from routes would give an importing error.
# Because it would want to import app that would not yet exist.

# After Blueprints we do not need that.
# from flaskblog import routes

# from flaskblog.main.routes import main
# from flaskblog.users.routes import users
# from flaskblog.posts.routes import posts

# app.register_blueprint(main)
# app.register_blueprint(users)
# app.register_blueprint(posts)

# After moving config to config.py
# Everything except the extensions is moved here.
# The reason why we do not move extentions to the functions is
# we want them to be created outside of the function, but we still
# want to initialize these extenstions inside of the function with the application.
# Flask documentation:
# This is so that the extension object does not initially get bound to the application
# Using this design patter no application specific state is stored on the extension object
# so one extension object can be used for multiple apps.


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskapp.main.routes import main
    from flaskapp.users.routes import users
    from flaskapp.social.routes import social
    from flaskapp.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(social)
    app.register_blueprint(errors)

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)

    from flaskapp.social.routes import MyView

    with app.app_context():
        db.create_all()
        app.add_url_rule('/new2', view_func=MyView.as_view('myview'))

    return app

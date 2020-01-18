from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flaskapp.config import Config


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


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from flaskapp.main.routes import main
    from flaskapp.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app

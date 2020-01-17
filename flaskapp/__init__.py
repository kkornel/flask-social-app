from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flaskapp.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from flaskapp.main.routes import main
    # from flaskapp.users.routes import users

    app.register_blueprint(main)
    # app.register_blueprint(users)

    return app

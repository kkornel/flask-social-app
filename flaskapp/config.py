import os


# Initially all configuration was in __int__.py,
# but if we want to run our app with different congiruation,
# we can make config.py classes based file.
# So our configration will be in one object and then we can use
# inheritance to specify even more configuration classes.


class Config:
    DEBUG = False
    # This should also be enviroment variable.
    # SECRET_KEY = '046e22b94eeaa82d1a6d721f0da941ec'
    SECRET_KEY = os.environ.get('MT_FLASK_APP_SECRET_KEY')
    # This should also be enviroment variable.
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/mt_flask_app'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'MT_FLASK_SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    # RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}


class DevelopmentConfig(Config):
    DEBUG = True

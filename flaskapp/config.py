import os


# Initially all configuration was in __int__.py,
# but if we want to run our app with different congiruation,
# we can make config.py classes based file.
# So our configration will be in one object and then we can use
# inheritance to specify even more configuration classes.


class Config:
    DEBUG = False
    # This should also be enviroment variable.
    # SECRET_KEY = '6107238231997648b4a5a6290e590fde'
    # This should also be enviroment variable.
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASS')


class DevelopmentConfig(Config):
    DEBUG = True

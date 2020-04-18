import os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
# Initially all configuration was in __int__.py,
# but if we want to run our app with different congiruation,
# we can make config.py classes based file.
# So our configration will be in one object and then we can use
# inheritance to specify even more configuration classes.


class Config:
    DEBUG = False
    SECRET_KEY = os.getenv('FLASK_SOCIAL_APP_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'FLASK_SOCIAL_APP_SQLALCHEMY_DATABASE_URI_POSTGRES')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER_POSTS_IMGS = 'static\posts_imgs'
    UPLOAD_FOLDER_PROFILES_IMGS = 'static\profiles_imgs',
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')
    MAIL_DEFAULT_SENDER = 'noreply@demo.com'
    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
    SECURITY_RESET_PASSWORD_SALT = os.getenv('SECURITY_RESET_PASSWORD_SALT')
    SECURITY_VERIFY_EMAIL_SALT = os.getenv('SECURITY_VERIFY_EMAIL_SALT')


class DevelopmentConfig(Config):
    DEBUG = True


class DeploymentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'FLASK_SOCIAL_APP_SQLALCHEMY_DATABASE_URI_SQLITE')


class TestConfig(DevelopmentConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tests.db'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
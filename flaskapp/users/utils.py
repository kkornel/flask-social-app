import os
import secrets
import re

from PIL import Image
from flask import url_for, current_app, render_template
from flask_mail import Message

from flaskapp import mail


def check_password_strength(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"\W", password) is None

    # overall result
    password_ok = not (length_error or digit_error or uppercase_error
                       or lowercase_error or symbol_error)

    # TODO uncomment later
    return password_ok
    # return True


def send_email(to, subject, template):
    msg = Message(subject,
                  recipients=[to],
                  html=template,
                  sender=current_app.config['MAIL_DEFAULT_SENDER'])
    mail.send(msg)

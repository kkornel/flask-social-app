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
    password_ok = not (
        length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

    # TODO uncomment later
    # return password_ok
    return True


def save_image(form_image):
    random_hex = secrets.token_hex(8)
    # splitext returns filename and extension, but we don't need
    # filename so we are using _
    _, file_extension = os.path.splitext(form_image.filename)
    image_fn = random_hex + file_extension
    image_path = os.path.join(
        current_app.root_path, 'static/profile_imgs', image_fn)
    output_size = (125, 125)
    img = Image.open(form_image)
    img.thumbnail(output_size)
    img.save(image_path)
    return image_fn


def send_reset_password_email(user):
    token = user.get_token(3600,
                           current_app.config['SECURITY_RESET_PASSWORD_SALT'])
    reset_url = url_for('users.reset_password_token',
                        token=token,
                        _external=True)
    html = render_template('users/mail_reset_password.html',
                           reset_url=reset_url)
    subject = 'Password Reset Request'
    send_email(user.email, subject, html)


def send_verification_email(user):
    token = user.get_token(None,
                           current_app.config['SECURITY_VERIFY_EMAIL_SALT'])
    confirm_url = url_for('users.confirm_email',
                          token=token,
                          _external=True)
    html = render_template('users/mail_verify_email.html',
                           confirm_url=confirm_url)
    subject = 'Please confirm your email'
    send_email(user.email, subject, html)


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

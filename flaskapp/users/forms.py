from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from flaskapp.models import User

# When we use this forms we need to set a secret key for our application.
# It will protect against modyfing cookies, and CRSF attacks etc.
# We set this in 'flaskblog.py' app.config[]
# If we do not specify secret key, we get error while
# visiting page with tag: {{ form.hidden_tag() }}


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Validation has to be in form:
    # def validate_field(self, field):
    #     if True:
    #         raise ValidationError('Validation Message')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Forgot password?')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Sorry.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    # Uses secure cookie to stay logged in for some time, after closing the browser.
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

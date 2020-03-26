from flask import Markup

from flask_login import current_user
from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from flaskapp.models.users import User
from flaskapp.users.utils import check_password_strength

# When we use this forms we need to set a secret key for our application.
# It will protect against modyfing cookies, and CRSF attacks etc.
# We set this in 'flaskblog.py' app.config[]
# If we do not specify secret key, we will get error
# while visiting page with tag: {{ form.hidden_tag() }}


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'Email address'})
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=4, max=15)],
                           render_kw={'placeholder': 'Username'})
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw={'placeholder': 'Password'})
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={'placeholder': 'Password confirmation'})
    recaptcha = RecaptchaField(
        validators=[Recaptcha(message="Check the reCaptcha field.")])
    submit = SubmitField('Sign Up')

    # Validation has to be in form:
    # def validate_field(self, field):
    #     if True:
    #         raise ValidationError('Validation Message')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                # Markup(f'''That email is already in use. <a href="{{ url_for('users.reset_password_request') }}">Forgot Password?</a>'''))
                Markup(
                    f'''That email is already in use. <a href="http://127.0.0.1:5000/reset_password">Forgot Password?</a>'''
                ))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already in use.')

    def validate_password(self, password):
        is_password_strong = check_password_strength(password.data)
        if not is_password_strong:
            raise ValidationError('''Password must be:
                                  at least 8 chars long and has at least:
                                  1 digit
                                  1 symbol
                                  1 uppercase letter
                                  1 lowercase letter''')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'Email'})
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw={'placeholder': 'Password'})
    # Uses secure cookie to stay logged in for some time, after closing the browser.
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestPasswordResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'Email address'})
    recaptcha = RecaptchaField(
        validators=[Recaptcha(message="Check the reCaptcha field.")])
    submit = SubmitField('Request Pasword Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email address.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password',
                             validators=[DataRequired()],
                             render_kw={'placeholder': 'New password'})
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={'placeholder': 'New password confirmation'})
    submit = SubmitField('Reset Password')

    def validate_password(self, password):
        is_password_strong = check_password_strength(password.data)
        if not is_password_strong:
            raise ValidationError('''Password must be:
                                  at least 8 chars long and has at least:
                                  1 digit
                                  1 symbol
                                  1 uppercase letter
                                  1 lowercase letter''')


class ChangeEmailForm(FlaskForm):
    email = StringField('Email',
                        validators=[Email()],
                        render_kw={'placeholder': 'Email address'})
    current_password = PasswordField(
        'Current password',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Current password'})
    submit = SubmitField('Update email')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and current_user.email != user.email:
            raise ValidationError('That email is already in use.')

    def validate_current_password(self, current_password):
        is_correct = current_user.verify_password(current_password.data)
        if not is_correct:
            raise ValidationError('Wrong password.')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        'Current password',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Current password'})
    password = PasswordField('New Password',
                             validators=[DataRequired()],
                             render_kw={'placeholder': 'New password'})
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[EqualTo('password')],
        render_kw={'placeholder': 'New password confirmation'})
    submit = SubmitField('Change password')

    def validate_current_password(self, current_password):
        is_correct = current_user.verify_password(current_password.data)
        if not is_correct:
            raise ValidationError('Wrong password.')

    def validate_password(self, password):
        if password.data == '':
            return
        is_password_strong = check_password_strength(password.data)
        if not is_password_strong:
            raise ValidationError('''Password must be:
                                  at least 8 chars long and has at least:
                                  1 digit
                                  1 symbol
                                  1 uppercase letter
                                  1 lowercase letter''')


class PasswordVerifyForm(FlaskForm):
    current_password = PasswordField(
        'Current password',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Current password'})
    submit = SubmitField('Verify')

    def validate_current_password(self, current_password):
        is_correct = current_user.verify_password(current_password.data)
        if not is_correct:
            raise ValidationError('Wrong password.')


class ProfileDeleteForm(FlaskForm):
    submit = SubmitField('Delete account')


class ProfileUpdateForm(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=4, max=15)],
                           render_kw={'placeholder': 'Username'})
    bio = TextAreaField('Bio',
                        validators=[Length(max=300)],
                        render_kw={
                            'placeholder': 'Bio',
                            'class': 'form-control',
                            'rows': 4,
                            'style': 'resize:none;'
                        })
    city = StringField('City',
                       validators=[Length(max=100)],
                       render_kw={'placeholder': 'Where do you live?'})
    website = StringField('Website',
                          validators=[Length(max=40)],
                          render_kw={'placeholder': 'Do you have website?'})
    image = FileField('Update Profile Image',
                      validators=[FileAllowed(['jpg', 'png'])])
    delete_current_image = BooleanField('Delete current image?')
    submit = SubmitField('Update Profile')

    # Validation has to be in form:
    # def validate_field(self, field):
    #     if True:
    #         raise ValidationError('Validation Message')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and current_user.username != user.username:
            raise ValidationError('That username is already in use.')


# Code for commented section in 'users/profile_update.html'
# Also for commented 'edit_profile' route
# All fields (email, username, password, bio, ..., in one page)
class UpdateProfileForm(FlaskForm):
    email = StringField('Email',
                        validators=[Email()],
                        render_kw={'placeholder': 'Email address'})
    username = StringField('Username',
                           validators=[Length(min=4, max=15)],
                           render_kw={'placeholder': 'Username'})
    password = PasswordField('New Password',
                             render_kw={'placeholder': 'New password'})
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[EqualTo('password')],
        render_kw={'placeholder': 'New password confirmation'})
    bio = TextAreaField('Bio',
                        validators=[Length(max=300)],
                        render_kw={
                            'placeholder': 'Bio',
                            'class': 'form-control',
                            'rows': 4,
                            'style': 'resize:none;'
                        })
    city = StringField('City',
                       validators=[Length(max=100)],
                       render_kw={'placeholder': 'Where do you live?'})
    website = StringField('Website',
                          validators=[Length(max=40)],
                          render_kw={'placeholder': 'Do you have website?'})
    image = FileField('Update Profile Image',
                      validators=[FileAllowed(['jpg', 'png'])])
    delete_current_image = BooleanField('Delete current image?')
    submit = SubmitField('Update Profile')

    # Validation has to be in form:
    # def validate_field(self, field):
    #     if True:
    #         raise ValidationError('Validation Message')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and current_user.email != user.email:
            raise ValidationError('That email is already in use.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and current_user.username != user.username:
            raise ValidationError('That username is already in use.')

    def validate_password(self, password):
        if password.data == '':
            return
        is_password_strong = check_password_strength(password.data)
        if not is_password_strong:
            raise ValidationError('''Password must be:
                                  at least 8 chars long and has at least:
                                  1 digit
                                  1 symbol
                                  1 uppercase letter
                                  1 lowercase letter''')

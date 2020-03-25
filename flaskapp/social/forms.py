
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

class PostCreateForm(FlaskForm):
    content = TextAreaField('Content', 
                            validators=[DataRequired(), Length(max=280)], 
                            render_kw={'placeholder': 'What\'s up?', 
                                        'class': 'form-control', 
                                        'rows': 8, 
                                        'style': 'resize:none;'})
    location = StringField('Where are you at?', 
                            validators=[Length(max=40)], 
                            render_kw={'placeholder': 'Helsinki, Finland'})
    image = FileField('Got any photo?',
                      validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

class PostUpdateForm(FlaskForm):
    content = TextAreaField('Edit content:', 
                            validators=[DataRequired(), Length(max=280)], 
                            render_kw={'placeholder': 'What\'s up?', 
                                        'class': 'form-control', 
                                        'rows': 8, 
                                        'style': 'resize:none;'})
    location = StringField('Edit location:', 
                            validators=[Length(max=40)], 
                            render_kw={'placeholder': 'Helsinki, Finland'})
    image = FileField('Change current image for new one:',
                      validators=[FileAllowed(['jpg', 'png'])])
    delete_current_image = BooleanField('Delete current image?')
    submit = SubmitField('Update')

class PostDeleteForm(FlaskForm):
    submit = SubmitField('Delete')

class CommentCreateForm(FlaskForm):
    content = TextAreaField('Content', 
                            validators=[Length(min=1, max=280)], 
                            render_kw={'placeholder': 'Leave your comment',
                                        'class': 'form-control', 
                                        'rows': 3, 
                                        'cols': 10,
                                        'style':'resize:none;',})
    submit = SubmitField('Replay')

class CommentDeleteForm(FlaskForm):
    submit = SubmitField('Delete')
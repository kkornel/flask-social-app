
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

class PostCreateForm(FlaskForm):
    render_kw={}
    content = TextAreaField('Content', 
                            validators=[DataRequired(), Length(max=280)], 
                            render_kw={'placeholder': 'What\'s up?', 'class': 'form-control', 'rows': 8, 'style': 'resize:none;'})
    location = StringField('Location', 
                            validators=[Length(max=40)], 
                            render_kw={'placeholder': 'Helsinki, Finland'})
    image = FileField('Got any photo?',
                      validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post!')


# class PostCreateForm(forms.ModelForm):
#     # If using CrispyForms, the only way to change background of textarea
#     # is to define style here. With CSS selector it's not working.
#     content = forms.CharField(
#         label='',
#         max_length=280,
#         widget=forms.Textarea(
#             attrs={
#                 'rows': 4,
#                 # 'cols': 30,
#                 'style': 'resize:none;',
#                 #   'style': 'resize:none; background-color: #15181c; color: #d9d9d9;',
#                 'placeholder': 'What\'s up?',
#             }))
#     location = forms.CharField(
#         label='Where are you at?',
#         required=False,
#         max_length=40,
#         widget=forms.TextInput(attrs={
#             'placeholder': 'Helsinki, Finland',
#         }))
#     # To remove 'Currently photo' and 'Clear' field,
#     # use this after required: widget=forms.FileInput
#     image = forms.ImageField(label='Got any photo?',
#                              required=False,
#                              widget=forms.FileInput)

#     class Meta:
#         model = Post
#         fields = ['content', 'location', 'image']
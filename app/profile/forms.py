from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

from app import messages

class EditProfileForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        allowed = current_app.config.get('ALLOWED_EXTENSIONS', [])
        self.avatar.validators = [
            FileAllowed(allowed, message="Only images (png, jpg, jpeg, webp)!")
        ]    
    username = StringField(
        "Username:",
        validators=[
            DataRequired(),
            Length(min=3, max=24, message=messages.USERNAME_LENGTH_ERROR),
            Regexp(r"^[A-Za-z0-9_]+$", message=messages.USERNAME_CHAR_ERROR),
        ],
    )    
    about = TextAreaField(
        "About me",
        validators=[
            Length(min=0, max=140, message=messages.GENERAL_LENGTH_ERROR),
        ],
    )
    submit = SubmitField("Update")

    
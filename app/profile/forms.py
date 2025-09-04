from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

from app import messages

class EditProfileForm(FlaskForm):

    username = StringField("Username", validators=[
            DataRequired(),
            Length(min=3, max=24, message=messages.USERNAME_LENGTH_ERROR),
            Regexp(r'^[A-Za-z0-9_]+$', message=messages.USERNAME_CHAR_ERROR)
        ]
    )
    about = TextAreaField("About me", validators=[Length(min=0, max=140, message= messages.GENERAL_LENGTH_ERROR)])
    submit = SubmitField('Update')

class EditProfileForm(FlaskForm):
    username = StringField(
        "Username",
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

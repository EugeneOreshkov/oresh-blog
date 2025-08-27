import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import (
    ValidationError,
    DataRequired,
    Email,
    Regexp,
    EqualTo,
    Length,
)

from app import db, messages
from app.models import User

class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=24, message=messages.USERNAME_LENGTH_ERROR),
            Regexp(r'^[A-Za-z0-9_]+$', message=messages.USERNAME_CHAR_ERROR)
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, max=24, message=messages.PASSWORD_FIELD_ERROR)
        ]
    )

    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=24, message=messages.USERNAME_LENGTH_ERROR),
            Regexp(r'^[A-Za-z0-9_]+$', message=messages.USERNAME_CHAR_ERROR)
        ]
    )

    email = StringField(
        'Email',
        validators=[
        DataRequired(),
        Email(),
        Length(max=64, message=messages.EMAIL_MAX_LENGTH_ERROR)
        ]
    )

    phone = StringField(
        'Phone',
        validators=[
        DataRequired(),
        Regexp(r'^\+?[0-9]{10,15}$', message=messages.PHONE_REGEX_ERROR)
        ]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(),
        Length(min=8, max=24, message=messages.PASSWORD_FIELD_ERROR)
        ]
    )

    password2 = PasswordField(
        'Repeat your password',
        validators=[DataRequired(),
        Length(min=8, max=24, message=messages.PASSWORD_FIELD_ERROR),
        EqualTo('password', message=messages.PASSWORD_MATCH_ERROR)
        ]
    )

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError(messages.USERNAME_TAKEN_ERROR)

    def validate_email(self, email):
        email = db.session.scalar(sa.select(User).where(User.email == email.data))
        if email is not None:
            raise ValidationError(messages.EMAIL_TAKEN_ERROR)

    def validate_phone(self, phone):
        phone = db.session.scalar(sa.select(User).where(User.phone == phone.data))
        if phone is not None:
            raise ValidationError(messages.PHONE_TAKEN_ERROR)
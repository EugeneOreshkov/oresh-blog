from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Regexp(r'^\+?[0-9]{10}$', message = "Please enter a valid phone number")])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat your password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
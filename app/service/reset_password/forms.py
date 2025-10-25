from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Почта:', validators=[DataRequired(), Email()])
    submit = SubmitField('Получить код')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль:', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Сбросить пароль')
    
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = TextAreaField('Заголовок:', validators=[DataRequired(), Length(max=128)])
    body = TextAreaField('Содержимое:', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')
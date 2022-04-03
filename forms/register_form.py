from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    photo = FileField('Фото профиля', validators=[DataRequired()])
    submit = SubmitField('ОК')

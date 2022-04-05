from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import PasswordField, StringField, SubmitField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль (не менее 8 символов; обязательно цифры'
                             ' и буквы разного регистра)',
                             validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    photo = FileField('Фото профиля', validators=[FileRequired()])
    submit = SubmitField('ОК')

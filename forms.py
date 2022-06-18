from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from models import User


class LoginForm(FlaskForm):  # пишу свою форму поверх базовой формы из фласка
    username = StringField('Имя пользователя: ')
    password = PasswordField('Пароль: ')
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):  # форма регистрации на оснвое базовой формы из Flask
    username = StringField('Имя пользователя: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired()])
    password = PasswordField('Пароль: ', validators=[DataRequired()])
    password_again = PasswordField('Пароль (подтверждение): ',
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def check_username(self, username):
        # найду пользователя в Базе Данных
        user = User.query.filter_by(username=username.data).first()
        if user is not None:  # если пользователь есть в БД
            raise ValidationError('Пользователь с таким ником уже зарегистрирован!')

    def check_email(self, email):
        # найду пользователя в Базе Данных
        user = User.query.filter_by(email=email.data).first()
        if user is not None:  # если пользователь есть в БД
            raise ValidationError('Пользователь с такой почтой уже зарегистрирован!')


class UpdateUrlForm(FlaskForm):
    url = StringField('URL: ')
    submit = SubmitField('Обновить')
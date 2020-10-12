from flask_security.forms import (RegisterForm, LoginForm)
from wtforms import (StringField, PasswordField)


class UserRegisterForm(RegisterForm):
    firstName = StringField('first_name')
    lastName = StringField('last_name')


class UserLoginForm(LoginForm):
    lastName = StringField('last_name')
    firstName = StringField('first_name')
    password = PasswordField('password')

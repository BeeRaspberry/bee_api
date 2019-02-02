from flask_security.forms import RegisterForm
from wtforms import StringField


class UserRegisterForm(RegisterForm):
    firstName = StringField('First Name')
    lastName = StringField('Last Name')


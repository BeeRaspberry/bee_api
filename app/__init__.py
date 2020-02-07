from os import environ

from flask_cors import CORS
from flask import Flask
from flask_security import (Security, SQLAlchemyUserDatastore)
from flask_paranoid import Paranoid
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(environ.get('CONFIG_SETTINGS',
                                   "config.DevelopmentConfig"))
db = SQLAlchemy(app)
migrate = Migrate(app, db)
"""
CORS(app)
paranoid = Paranoid(app)
paranoid.redirect_view = '/'


if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
    from flask.ext.sslify import SSLify
    SSLify(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore,
                    login_form=UserLoginForm)
"""
from app import routes

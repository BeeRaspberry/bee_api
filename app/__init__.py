from os import environ
from os.path import (join, exists, abspath, dirname, exists)
from os import (environ)
import sys
import logging

from flask_cors import CORS
from flask import Flask
from flask_security import (Security, SQLAlchemyUserDatastore)
from flask_paranoid import Paranoid
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

if environ.get('CONFIG_FILE') and not exists(environ.get('CONFIG_FILE')):
    print('Config file, {}, not found ... exiting'.format(
        environ.get('CONFIG_FILE')))
    sys.exit(9)
    
app = Flask(__name__)

app.config.from_pyfile(environ.get('CONFIG_FILE') or 'config.cfg')

print('Database location: {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))

db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app)
"""paranoid = Paranoid(app)
paranoid.redirect_view = '/'


if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
    from flask.ext.sslify import SSLify
    SSLify(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore,
                    login_form=UserLoginForm)
"""

from app import routes

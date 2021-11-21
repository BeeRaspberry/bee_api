from os.path import (join, abspath, exists, dirname)
from os import (environ)
import sys
import logging

from flask_cors import CORS
from flask import Flask
from flask_security import (Security, SQLAlchemyUserDatastore)
from flask_paranoid import Paranoid
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

if environ.get('CONFIG_FILE'):
    config_file = join(abspath(dirname(__file__)), environ.get('CONFIG_FILE'))
else:
    config_file = join(abspath(dirname(__file__)), 'config.cfg')

if not exists(config_file):
    print('Config file, {}, not found ... exiting'.format(config_file))
    sys.exit(9)

APP = Flask(__name__)

APP.config.from_pyfile(config_file)

print('Database location: {}'.format(APP.config['SQLALCHEMY_DATABASE_URI']))

DB = SQLAlchemy(APP)

migrate = Migrate(APP, DB)

CORS(APP)
# paranoid = Paranoid(APP)
# paranoid.redirect_view = '/'
#
#
# if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
#    from flask.ext.sslify import SSLify
#    SSLify(APP)
#

from app import routes

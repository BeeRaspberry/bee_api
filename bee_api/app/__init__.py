import os

from flask_cors import CORS
from flask_restful import Api
from flask import Flask
from flask_security import (Security, SQLAlchemyUserDatastore)
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
CORS(app)
csrf = CSRFProtect(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'config.DevelopmentConfig'
)

travis = os.getenv('TRAVIS', None)
if travis:
    app_settings = 'config-sample.TestingConfig'

app.config.from_object(app_settings)

from database import (db)
from classes.user.model import (User, Role)
from classes.user.forms import (UserRegisterForm)
api = Api(app)

if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
    from flask.ext.sslify import SSLify
    SSLify(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore,
                    register_form=UserRegisterForm)
import routes


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

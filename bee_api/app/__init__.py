import os

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from flask import Flask

app = Flask(__name__)
CORS(app, resources=r'/*')

app_settings = os.getenv(
    'APP_SETTINGS',
    'bee_api.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#manager = Manager(app)
#manager.add_command('db', MigrateCommand)

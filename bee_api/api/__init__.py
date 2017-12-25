# project/server/__init__.py

import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import decimal
from dateutil import parser
import flask.json

from flask import Flask, jsonify, request

from flask_restful import Api
from flask_restless import ProcessingException
from flask_script import Manager
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate, MigrateCommand
#from bee_api.schema import *
from bee_api.models import db

app = Flask(__name__)
CORS(app, resources=r'/*')

app_settings = os.getenv(
    'APP_SETTINGS',
    'bee_api.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
#db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#country_schema = CountrySchema()
#countries_schema = CountrySchema(many=True)
#stateProvince_schema = StateProvinceSchema()
#stateProvinces_schema = StateProvinceSchema(many=True)
#location_schema = LocationSchema()
#locations_schema = LocationSchema(many=True)
#owner_schema = OwnerSchema()
#owners_schema = OwnerSchema(many=True)
#hive_schema = HiveSchema()
#hives_schema = HiveSchema(many=True)
#hiveData_schema = HiveDataSchema()
#hiveDatas_schema = HiveDataSchema(many=True)
import datetime
from sqlalchemy import *
from sqlalchemy.orm import (relationship, backref)
import jwt
from flask_security import UserMixin, RoleMixin
from bee_api.database import Base
from bee_api.app import bcrypt, app

#def create_tables(app2):
#    "Create tables, and return engine in case of further processing."
#    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
#    app.db.metadata.create_all(engine)
#    return engine


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
#    api = Column(String(255))
    firstName = Column(String(50))
    lastName = Column(String(50))
    phoneNumber = Column(String(20))
    locationId = Column(Integer, ForeignKey('location.id'))
    location = relationship('Location', backref='user')
    registeredOn = Column(DateTime, default=datetime.datetime.utcnow)
    active = Column(BOOLEAN())
    confirmed_at = Column(DateTime())
 #   roleId = Column(Integer, ForeignKey('role.id'))
 #   role = relationship('Role', backref='user')
#    roles = relationship('Role', secondary=roles_users,
#                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return "{} {}".format(self.firstName, self.lastName)

#    @validates('email')
#    def validate_email(self, key, address):
#        assert '@' in address
#        return address

    def __init__(self, email, password, firstName = None, lastName = None,
                 phoneNumber = None,  locationId = None, roleId=None,
                 api=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registeredOn = datetime.datetime.now()
        self.firstName = firstName
        self.lastName = lastName
        self.phoneNumber = phoneNumber
        self.locationId = locationId
        self.active = True
 #       self.roleId = roleId
 #       self.api = api
 #       if roles is None:
 #           roles = []
 #       self.roles = roles

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0,
                                seconds=app.config.get('SECRET_TIMEOUT')),
                'iat': datetime.datetime.utcnow(),
                'jti': self.id,
                'sub': self.id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                app.config.get('JWT_ALGORITHM')
            ).decode()
        except Exception as e:
            return e

#    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'),
                                 algorithms = app.config.get('JWT_ALGORITHM'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class StateProvince(Base):
    __tablename__ = 'stateProvince'
    id = Column(Integer, primary_key=True, autoincrement=True)
    countryId = Column(Integer, ForeignKey('country.id'))
    country = relationship('Country', backref='stateProvinces')
    name = Column(String(200))
    abbreviation = Column(String(10))

    def __repr__(self):
        return self.name


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    streetAddress = Column(String(200))
    city = Column(String(200))
    postalCode = Column(String(20))
    stateProvinceId = Column(Integer, ForeignKey('stateProvince.id'))
    stateProvince = relationship('StateProvince', backref='location')


class BlacklistToken(Base):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(500), unique=True, nullable=False)
    blacklisted_on = Column(DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


class Hive(Base):
    __tablename__ = "hive"
    id = Column(Integer, primary_key=True)
    ownerId = Column(Integer, ForeignKey('user.id'))
    owner = relationship('User', backref='hives')
# Hive Id equals the local hive id.
    hiveId = Column(Integer)
# Hive location may differ from the location of the bee keeper
    locationId = Column(Integer, ForeignKey('location.id'))
    location = relationship('Location', backref='hives')
    dateCreated = Column(DateTime, default=datetime.datetime.utcnow)
    lastUpdate = Column(DateTime, default=datetime.datetime.utcnow)
#    door_open = Column(Boolean, server_default=True)


class HiveData(Base):
    __tablename__ = "hiveData"
    id = Column(Integer, primary_key=True)
    hiveId = Column(Integer, ForeignKey('hive.id'))
    hive = relationship('Hive', backref='hiveData')
    dateCreated = Column(DateTime, default=datetime.datetime.utcnow)
    temperature = Column(Numeric)
    humidity = Column(Numeric)
    sensor = Column(Integer)
    outdoor = Column(BOOLEAN)


# Define models
#roles_users = db.Table('roles_users',
#        Column('user_id', Integer(), db.ForeignKey('user.id')),
#        Column('role_id', Integer(), db.ForeignKey('role.id')))

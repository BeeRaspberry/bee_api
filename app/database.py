import datetime
from sqlalchemy import (Column, Integer, String, Numeric, BOOLEAN,
                        ForeignKey, DateTime)
from sqlalchemy.orm import (relationship, backref)
from flask_security import (UserMixin, RoleMixin)

from app import DB


class Country(DB.Model):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))
    shortName = Column(String(10))
#    state_provinces = relationship("StateProvince", backref="countries")


class StateProvince(DB.Model):
    __tablename__ = 'stateProvince'
    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(Integer, ForeignKey("country.id"))
    countries = relationship("Country", backref="state_provinces")
    name = Column(String(200))
    abbreviation = Column(String(10))

    def __repr__(self):
        return self.name


class Location(DB.Model):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    street_address = Column(String(200))
    city = Column(String(200))
    postal_code = Column(String(20))
    stateProvinceId = Column(Integer, ForeignKey('stateProvince.id'))
    state_province = relationship('StateProvince', backref='location')


class Hive(DB.Model):
    __tablename__ = "hive"
    id = Column(Integer, primary_key=True)
    ownerId = Column(Integer, ForeignKey('user.id'))
    owner = relationship('User', backref='hives')
# Hive location may differ from the location of the bee keeper
    locationId = Column(Integer, ForeignKey('location.id'))
    location = relationship('Location', backref='hives')
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    last_update = Column(DateTime, default=datetime.datetime.utcnow)
#    door_open = Column(Boolean, server_default=True)


class HiveData(DB.Model):
    __tablename__ = "hiveData"
    id = Column(Integer, primary_key=True)
    hiveId = Column(Integer, ForeignKey('hive.id'))
    hive = relationship('Hive', backref='hiveData')
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    temperature = Column(Numeric)
    humidity = Column(Numeric)
    sensor = Column(Integer)
    outdoor = Column(BOOLEAN)


class RolesUsers(DB.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(DB.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(DB.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    firstName = Column(String(50))
    lastName = Column(String(50))
    phoneNumber = Column(String(20))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    locationId = Column(Integer, ForeignKey('location.id'))
    location = relationship('Location', backref='user')
    registeredOn = Column(DateTime, default=datetime.datetime.utcnow)
    active = Column(BOOLEAN())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

    def __repr__(self):
        return "{} {}".format(self.firstName, self.lastName)

#    def set_password(self, password):
#        self.password = generate_password_hash(password)


class BlacklistToken(DB.Model):
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

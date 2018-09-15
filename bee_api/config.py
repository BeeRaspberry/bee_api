import os


class BaseConfig:
    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE_TYPE = 'sqlite'
    DATABASE_NAME = 'beehive'
    DATABASE_USER = None
    DATABASE_PASSWORD = None
    DATABASE_PORT = None
    DATABASE_HOST = None
    if DATABASE_TYPE == 'sqlite':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, DATABASE_NAME)
    else:
        SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
            DATABASE_TYPE, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST,
            DATABASE_PORT, DATABASE_NAME)

    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    SECRET_TIMEOUT = int(os.getenv('SECRET_TIMEOUT', '900'))
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13

# Flask-security settings
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'mySalt'
    SECURITY_TOKEN_AUTHENTICATION_KEY = 'auth_token'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_TOKEN_MAX_AGE = 1800
    SECURITY_TRACKABLE = False
    SECURITY_RECOVERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_REGISTERABLE = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
#    JWT_ALGORITHM = os.getenv('ALGORITHM', 'HS256')
#    JWT_IDENTITY_CLAIM = os.getenv('ID_CLAIM', 'sub')


class DevelopmentConfig(BaseConfig):
    basedir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    DATABASE_TYPE = 'postgresql'
    DATABASE_USER = 'bee_db'
    DATABASE_PASSWORD = '10ff1ce0!'
    DATABASE_PORT = 5433
    DATABASE_HOST = 'localhost'
    DATABASE_NAME = 'beehive_dev'
    if DATABASE_TYPE == 'sqlite':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, DATABASE_NAME)
    else:
        SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
            DATABASE_TYPE, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST,
            DATABASE_PORT, DATABASE_NAME)


class TestingConfig(BaseConfig):
    basedir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    DATABASE_TYPE = 'sqlite'
    DATABASE_USER = None
    DATABASE_PASSWORD = None
    DATABASE_PORT = None
    DATABASE_HOST = None
    DATABASE_NAME = 'beehive_test'
    if DATABASE_TYPE == 'sqlite':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, DATABASE_NAME)
    else:
        SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
            DATABASE_TYPE, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST,
            DATABASE_PORT, DATABASE_NAME)

    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    SECRET_KEY = 'my_precious_production'
    DATABASE_TYPE = 'postgresql'
    DATABASE_USER = None
    DATABASE_PASSWORD = None
    DATABASE_PORT = None
    DATABASE_HOST = None
    DATABASE_NAME = 'beehive'
    DEBUG = False
    if DATABASE_TYPE == 'sqlite':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, DATABASE_NAME)
    else:
        SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
            DATABASE_TYPE, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST,
            DATABASE_PORT, DATABASE_NAME)

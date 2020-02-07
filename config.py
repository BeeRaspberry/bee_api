import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_NAME = os.environ.get('APP_NAME') or 'bee_mine'
    basedir = os.path.abspath(os.path.dirname(__file__))

    DATABASE_TYPE = os.environ.get('DATABASE_TYPE') or 'sqlite'
    DATABASE_NAME = os.environ.get('DATABASE_NAME') or 'beehive_migrate'
    DATABASE_USER = os.environ.get('DATABASE_USER') or 'root'
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD') or 'mypassword'
    DATABASE_PORT = os.environ.get('DATABASE_PORT') or None
    DATABASE_HOST = os.environ.get('DATABASE_HOST') or '127.0.0.1'

    if DATABASE_TYPE == 'sqlite':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, DATABASE_NAME)
    else:
        SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
            DATABASE_TYPE, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST,
            DATABASE_PORT, DATABASE_NAME)

    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    SECRET_TIMEOUT = int(os.getenv('SECRET_TIMEOUT', '900'))
    DEBUG = False
    TESTING = False
    BCRYPT_LOG_ROUNDS = 13

    INFLUXDB_HOST = os.environ.get('INFLUXDB_HOST') or 'localhost'
    INFLUXDB_PORT = os.environ.get('INFLUXDB_PORT') or 8086
    INFLUXDB_DATABASE =os.environ.get('INFLUXDB_DATABASE') or 'hivedata'
    INFLUXDB_PASSWORD = os.environ.get('INFLUXDB_PASSWORD') or 'mypassword'
    INFLUXDB_USER = os.environ.get('INFLUXDB_USER') or 'root'

# Flask-security settings
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = os.environ.get('PASSWORD_SALT') or 'mySalt'
    SECURITY_TOKEN_AUTHENTICATION_KEY = 'auth_token'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_TOKEN_MAX_AGE = 1800
    SECURITY_TRACKABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_USER_IDENTITY_ATTRIBUTES = 'email'
    SECURITY_LOGIN_URL = '/login'
    WTF_CSRF_ENABLED = False

    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.sendgrid.net'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 587
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') or False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # Admin account
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'password123#'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@example.com'
    EMAIL_SUBJECT_PREFIX = '[{}]'.format(APP_NAME)
    EMAIL_SENDER = '{app_name} Admin <{email}>'.format(
        app_name=APP_NAME, email=MAIL_USERNAME)

    SOCIAL_GOOGLE = {
        'consumer_key': "930191446877-t7cjmetllp6lfhd7tipun851e9g2cute.apps.googleusercontent.com",
        'consumer_secret': "s_E0V1fJFNCSXgG1v3igkNDS"
    }


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4

    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    SECRET_KEY = 'my_precious_production'

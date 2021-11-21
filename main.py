from os.path import (join, exists, abspath, dirname)
from glob import glob
from sqlalchemy.exc import *
from flask_fixtures.loaders import JSONLoader
from flask_fixtures import load_fixtures
import click
from app import (APP, DB)

@APP.cli.command('initdb')
def init_db():
    DB.create_all()


@APP.cli.command('seed')
@click.argument('seed_dir', default='seed')
def seed_command(seed_dir):
    """Load seed data"""
    if not exists(seed_dir):
        print("Directory, {}, doesn't exist ... exiting".format(seed_dir))
        return False

    base_dir = abspath(dirname(__file__))

    for fixture_file in glob(join(base_dir, seed_dir, '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        try:
            load_fixtures(DB, fixtures)
        except IntegrityError as err:
            print('It appears, {}, was already processed'.format(
                fixture_file))
     #   except sqlite3.OperationalError as sql_error:
     #       print('Problem with database connection, {}'.format(
     #           db.engine.
     #       ))


if __name__ == '__main__':
    APP.run()

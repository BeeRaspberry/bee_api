""" Helper for Loading Database Data """
from os.path import (join, abspath, dirname)
from glob import glob
from flask_fixtures.loaders import JSONLoader
from flask_fixtures import load_fixtures
import pytest

from app import DB

@pytest.fixture(scope='function')
def init_database():
    """Initializes the database """
    DB.drop_all()
    DB.create_all()

    base_dir = join(abspath(dirname(__file__)), '..', '..')

    for fixture_file in glob(join(base_dir, 'seed', '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        load_fixtures(DB, fixtures)

    for fixture_file in glob(join(base_dir, 'seed', 'demo', '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        load_fixtures(DB, fixtures)

    yield DB

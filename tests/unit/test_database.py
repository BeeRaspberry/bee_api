from unittest import TestCase
import pytest
from app import (db, app)
from app.database import (Country, StateProvince, Location, HiveData, Hive,
                          User, Role)


@pytest.fixture(scope='module')
def init_database():
    from os.path import (abspath, dirname, join)
    from glob import glob
    from flask_fixtures.loaders import JSONLoader
    from flask_fixtures import load_fixtures

    print('Database location: {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))
    db.drop_all()
    db.create_all()

    base_dir = abspath(dirname(__file__))

    for fixture_file in glob(join(base_dir, '..', 'fixtures', '*.json')):
        fixtures = JSONLoader().load(fixture_file)
        load_fixtures(db, fixtures)

    yield db


@pytest.fixture
def add_location():
    def _add_location(street_address, city, postal_code, stateProvinceId):
        temp = Location(street_address=street_address,
                        city=city,
                        postal_code=postal_code,
                        stateProvinceId=stateProvinceId)
        db.session.add(temp)
        db.session.commit()
        return db.session.query(Location).filter_by(postal_code=postal_code).one()

    return _add_location


@pytest.fixture(scope='module')
def add_role():
    def _add_role(name, description):
        temp = Role(name=name, description=description)
        db.session.add(temp)
        db.session.commit()
        return db.session.query(Role).filter_by(name=name).one()

    return _add_role


@pytest.mark.usefixtures("init_database")
class TestCountryTable(TestCase):
    def test_country_all(self):
        result = db.session.query(Country).all()
        self.assertGreaterEqual(len(result), 3)

    def test_country_short_name(self):
        result = db.session.query(Country).filter_by(name="Canada").one()
        self.assertEqual(result.shortName, "CA")

    def test_new_country(self):
        self.assertIsNotNone(Country(name='Great Britain', shortName="GB"))


@pytest.mark.usefixtures("init_database")
class TestStateProvinceTable(TestCase):
    def test_state_province_all(self):
        result = db.session.query(StateProvince).all()
        self.assertGreaterEqual(len(result), 50)

    def test_state_province_abbreviation(self):
        result = db.session.query(StateProvince).filter_by(
            name="Washington").one()
        self.assertEqual(result.abbreviation, "WA")

    def test_new_state_province(self):
        country = db.session.query(Country).filter_by(name="Canada").one()
        self.assertIsNotNone(StateProvince(name="Mickey Land",
                                           abbreviation="ML",
                                           country=country))


@pytest.mark.usefixtures("init_database")
class TestLocationTable(TestCase):
    def test_location_all(self):
        result = db.session.query(Location).all()
        self.assertGreaterEqual(len(result), 1)

    def test_location_city(self):
        location = db.session.query(Location).filter_by(city="Boston").one()
        self.assertEqual(location.stateProvinceId, 21)

    def test_new_location(self):
        self.assertIsNotNone(Location(city="Orleans",
                                      street_address="One Main St.",
                                      stateProvinceId=10,
                                      postal_code="12345"))

 
@pytest.mark.usefixtures('init_database')
class TestHiveTable(TestCase):
    def test_new_hive(self):
        new_location = Location(street_address="street_address",
                                city="Boston",
                                postal_code="23456",
                                stateProvinceId=11)
        new_user = User(email="test@test.com")
        new_hive = Hive(owner=new_user, location=new_location)
        db.session.add(new_location)
        db.session.add(new_user)
        db.session.add(new_hive)
        db.session.commit()

        self.assertEqual(new_hive.location, new_location)
        self.assertEqual(new_hive.owner, new_user)
        result = db.session.query(Hive).all()
        self.assertEqual(len(result), 1)

"""
@pytest.fixture(scope='module')
@pytest.mark.usefixtures('new_location', 'new_role')
def new_user(new_location, new_role):
    return User(email='bee.mine@bee.org', password='password',
                firstName='Queen', lastName='Bee', phoneNumber='1234567890',
                location=new_location, roles=new_role)


@pytest.fixture(scope='module')
@pytest.mark.usefixtures('new_location', 'new_user')
def new_hive(new_location, new_user):
    return Hive(location=new_location, owner=new_user)


@pytest.mark.usefixtures('new_role')
def test_new_role(new_role):
    self.assertEqual(new_role[0].name, 'queen')
    self.assertEqual(new_role[0].description, 'Queen bee')


@pytest.mark.usefixtures('new_user', 'new_role', 'new_location')
def test_new_user(new_user, new_role, new_location):
    assert new_user.firstName == 'Queen'
    assert new_user.lastName == 'Bee'
    assert new_user.email == 'bee.mine@bee.org'
    assert new_user.password == 'password'
    assert new_user.phoneNumber == '1234567890'
    assert new_user.location == new_location
    assert new_user.roles == new_role


@pytest.mark.usefixtures('new_hive')
def test_new_hive_data(new_hive):
    hive_data = HiveData(hive=new_hive, temperature=90.0, humidity=50.4,
                         sensor=1, outdoor=False)
    assert hive_data.hive == new_hive
    assert hive_data.humidity == 50.4
    assert hive_data.temperature == 90.0
    assert hive_data.sensor == 1
    assert hive_data.outdoor is False

    hive_data = HiveData(hive=new_hive, temperature=80.0, humidity=40.4,
                         sensor=2, outdoor=True)
    assert hive_data.hive == new_hive
    assert hive_data.humidity == 40.4
    assert hive_data.temperature == 80.0
    assert hive_data.sensor == 2
    assert hive_data.outdoor is True

"""

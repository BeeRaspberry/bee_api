from unittest import TestCase
import pytest
from app import DB
from app.database import (Country, StateProvince, Location, HiveData, Hive,
                          User, Role)


#@pytest.fixture(scope='module')
#@pytest.mark.usefixtures("init_database")
#def new_location(init_database):
#    def _add_location(street_address, city, postal_code, stateProvinceId):
#        temp = Location(street_address=street_address,
#                        city=city,
#                        postal_code=postal_code,
#                        stateProvinceId=stateProvinceId)
#        init_database.session.add(temp)
#        init_database.session.commit()
#        return init_database.session.query(Location).filter_by(
#            postal_code=postal_code).one()
#
#    return _add_location
#
#
#@pytest.fixture(scope='module')
#@pytest.mark.usefixtures("init_database")
#def new_role(init_database):
#    def _add_role(name, description):
#        temp = Role(name=name, description=description)
#        DB.session.add(temp)
#        DB.session.commit()
#        return DB.session.query(Role).filter_by(name=name).one()
#
#    return _add_role
#
#
#@pytest.fixture(scope='module')
#@pytest.mark.usefixtures('new_location', 'new_role')
#def new_user(new_location, new_role):
#    return User(email='bee.mine@bee.org', password='password',
#                firstName='Queen', lastName='Bee', phoneNumber='1234567890',
#                location=new_location, roles=new_role)
#
#
#@pytest.fixture(scope='module')
#@pytest.mark.usefixtures('new_location', 'new_user')
#def new_hive(new_location, new_user):
#    return Hive(location=new_location, owner=new_user)
#
#
@pytest.mark.usefixtures("init_database")
class TestCountryTable(TestCase):
    '''Test Country Table'''
    def test_country_all(self):
        '''Test Query gets the correct number of rows'''
        result = DB.session.query(Country).all()
        self.assertEqual(len(result), 3, "Country List not equal 3")

    def test_country_short_name(self):
        '''Test Query to check for Short Name'''
        result = DB.session.query(Country).filter_by(name="Canada").first()
        self.assertEqual(result.shortName, "CA")

    def test_new_country(self):
        self.assertIsNotNone(Country(name='Great Britain', shortName="GB"))


@pytest.mark.usefixtures("init_database")
class TestStateProvinceTable(TestCase):
    '''Test State Province Table'''
    def test_state_province_all(self):
        '''Test Query gets the correct number of rows'''
        result = DB.session.query(StateProvince).all()
        self.assertGreaterEqual(len(result), 50)

    def test_state_province_abbreviation(self):
        '''Test Query to check for State Abbreviation'''
        result = DB.session.query(StateProvince).filter_by(
            name="Washington").first()
        self.assertEqual(result.abbreviation, "WA")

    def test_new_state_province(self):
        country = DB.session.query(Country).filter_by(name="Canada").first()
        self.assertIsNotNone(StateProvince(name="Mickey Land",
                             abbreviation="ML",
                             country_id=country.id))


@pytest.mark.usefixtures("init_database")
class TestLocationTable(TestCase):
    '''Test Location Table'''
    def test_location_all(self):
        '''Test Query gets the correct number of rows'''
        result = DB.session.query(Location).all()
        self.assertGreaterEqual(len(result), 1)

    def test_location_city(self):
        ''' Test Query of City'''
        location = DB.session.query(Location).filter_by(city="Boston").first()
        self.assertEqual(location.stateProvinceId, 21)

    def test_new_location(self):
        ''' Test new Location '''
        self.assertIsNotNone(Location(city="Orleans",
                             street_address="One Main St.",
                             stateProvinceId=10,
                             postal_code="12345"))


@pytest.mark.usefixtures("init_database")
class TestHiveTable(TestCase):
    '''Test Hive Table'''
    def test_new_hive(self):
        '''Test New Hive'''
        new_location = Location(street_address="street_address",
                                city="Boston",
                                postal_code="23456",
                                stateProvinceId=11)
        new_user = User(email="test@test.com")
        new_hive = Hive(owner=new_user, location=new_location)
        DB.session.add(new_location)
        DB.session.add(new_user)
        DB.session.add(new_hive)
        DB.session.commit()

        result = DB.session.query(Hive).all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].location, new_location)
        self.assertEqual(result[0].owner, new_user)

"""
def test_new_role(new_role):
    TestCase().assertEqual(new_role[0].name, 'queen')
    TestCase().assertEqual(new_role[0].description, 'Queen bee')

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

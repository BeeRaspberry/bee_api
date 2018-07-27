import sys
import logging
from ast import literal_eval
from bee_api.database import db_session, Base
from bee_api.models import Country, StateProvince, Location
from bee_api.app import app

log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():

#    log.info('Insert Country data in database')
#    with open('fixtures/country.json', 'r') as file:
#        data = literal_eval(file.read())
#        for record in data:
#            country = Country(**record)
#            db_session.add(country)
#        db_session.commit()

    log.info('Insert State data in database')
    with open('fixtures/state_province.json', 'r') as file:
        data = literal_eval(file.read())
        for record in data:
            province = StateProvince(**record)
            db_session.add(province)
        db_session.commit()

    log.info('Insert Location data in database')
    with open('fixtures/location.json', 'r') as file:
        data = literal_eval(file.read())
        for record in data:
            location = Location(**record)
            db_session.add(location)
        db_session.commit()

if __name__ == '__main__':
    main()
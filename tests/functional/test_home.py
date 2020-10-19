import json
import requests
from tests.support.assertions import assert_valid_schema

def run_query(uri, query, statusCode, headers):
    request = requests.post(uri, json={'query': query}, headers=headers)
    if request.status_code == statusCode:
        return request.json()
    else:
        raise Exception(f"Unexpected status code returned: {request.status_code}")

def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    json_data = json.loads(response.data.decode('utf-8'))


def test_country_list(test_client):
    query = '''
         query CountryQuery {
             countryList {
             edges {
             node {
                 name
             }
         }
         }
     }
    '''
    response = run_query('http://localhost:5000/graphql', query, 200, '')

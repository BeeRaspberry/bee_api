import os
import glob
import json
from flask_fixtures import load_fixtures
from flask_fixtures.loaders import JSONLoader
from bee_api.jwt.auth import app
import unittest
import tempfile


class BeeWebTestCase(unittest.TestCase):
    def test_add_hivedata(self):

        json_data = dict(username="joe",password="pass")
        rv = self.app.post('/auth/',
                           data=json.dumps(json_data),
                           content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        json_resp = json.loads(rv.data)
        self.assertEqual(json_resp['message'], 'Created Hive Data Entry')


if __name__ == '__main__':
    unittest.main()
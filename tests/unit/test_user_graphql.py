""" Unit Test Module for Graphql """
import sys
from os.path import (join, abspath, dirname)
from json import (loads, dumps)
import unittest
import pytest
from graphene.test import Client
from testclass.testclass import TestClass
from app.schema import SCHEMA

@pytest.mark.usefixtures("init_database")
class TestUserGraphGL(unittest.TestCase):
    """Test Suite for testing User GraphQL"""
    dir_name = join(abspath(dirname(__file__)), 'files')
    client = Client(SCHEMA)
    client

    def test_user_email_login(self):
        """Execute user login test"""
        test_data = TestClass(self.dir_name,
                              sys._getframe(  ).f_code.co_name)
        test_data.load_files()

        response = self.client.execute(
            test_data.get_send_request(),
            variables=test_data.get_variables())

        print(response)
#        self.assertEqual(response['data']['role'], 'user')
#        self.assertEqual(response['data']['name'], 'Mickey Mouse')
#        self.assertIsNotNone(response['data']['accessToken'])
#        self.assertIsNotNone(response['data']['refreshToken'])


if __name__ == '__main__':
    unittest.main()

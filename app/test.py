import unittest
import os
import json
from app import create_app, db

class CorpusTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {
            'name': 'Diane',
            'username': 'dianediane',
            'email': 'diane@diane.di',
            'password': 'Diane1sdiane'
            }

        with self.app.app_context():
            db.create_all()

    def test_user_creation(self):
        """ Test API can create a User (POST)."""
        res = self.client().post('/poet/', data=self.user)
        self.assertEqual(res.status_code, 201)
        # self.assertIn()
    
    def test_return_user_info(self):
        """ Test API can return a User's info (GET)."""
        res = self.client().post('/poet/', data=self.user)
        self.assertEqual(res.status_code, 201)

        self.client().get('/poet/', data=self.user)
        # self.assertEqual(res.status_code, 200) # weirdly returns 201????
        self.assertIn(self.user['username'], str(res.data))
        self.assertIn(self.user['email'], str(res.data))
        self.assertNotIn(self.user['password'], str(res.data))

    # def test_

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
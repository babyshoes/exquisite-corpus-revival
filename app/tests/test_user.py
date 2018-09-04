import unittest
import os
import json
import re
from app import app, db
from services import CorpusAnimator

class CorpusTestCase(unittest.TestCase):
    def setUp(self):
        # self.app = app.create_app(config_name="testing")
        self.app = app
        self.client = self.app.test_client
        self.user = {
            'name': 'Diane',
            'username': 'dianediane',
            'email': 'diane@diane.di',
            'password': 'Diane1sdiane'
            }
        self.user2 = {
            'name': 'Lee',
            'username': 'leandroid',
            'email': 'imabutt@lee.edu',
            'password': 'Le3L3eLe3'
        }
        self.user3 = {
            'name': 'Steph',
            'username': 'steviewonder',
            'email': 'steph@stef.com',
            'password': 'steponmefungus'
        }

        self.corpus = {
            'title': ''
        }

        with self.app.app_context():
            db.create_all()

    def create_user(self, user_data):
        return self.client().post('/poet/', data=user_data)

    def get_user_id(self, user_data):
        user_info = self.client().get('/poet/', data=user_data).data
        user_info = self.unpack_json(user_info)
        return int(user_info['id'])

    def create_round(self):
        return self.client().post('/round/')

    def create_corpus(self, poet_id):
        corpus_data = {'poet_id': poet_id, **self.corpus}
        return self.client().post('/corpus/', data=corpus_data)
    
    def unpack_json(self, json):
        output = re.findall(r"\{([\w\W]*)\}", str(json))[0]
        return dict([val.split(':') for val in output.replace('"', '').split(',')])

    def test_user_creation(self):
        """ Test API can create a User (POST)."""
        # import pdb;pdb.set_trace()
        res = self.create_user(self.user)
        self.assertEqual(res.status_code, 201)
        # self.assertIn()
    
    def test_return_user_info(self):
        """ Test API can return a User's info (GET)."""
        res = self.create_user(self.user)

        poet_data = self.client().get('/poet/', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn(self.user['username'], str(res.data))
        self.assertIn(self.user['email'], str(res.data))
        self.assertNotIn(self.user['password'], str(res.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
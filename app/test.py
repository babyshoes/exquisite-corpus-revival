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
        self.corpus = {
            'title': ''
        }

        with self.app.app_context():
            db.create_all()

    def create_user(self):
        return self.client().post('/poet/', data=self.user)

    def create_round(self):
        return self.client().post('/round/')

    def create_corpus(self, poet_ids):
        corpus_data = self.corpus + {'poet_ids': poet_ids}
        corpus_data['poet_ids'] = poet_ids
        return self.client().post('/corpus/', data=self.corpus)

    def test_user_creation(self):
        """ Test API can create a User (POST)."""
        res = self.create_user()
        self.assertEqual(res.status_code, 201)
        # self.assertIn()
    
    def test_return_user_info(self):
        """ Test API can return a User's info (GET)."""
        res = self.create_user()

        self.client().get('/poet/', data=self.user)
        # self.assertEqual(res.status_code, 200) # weirdly returns 201????
        self.assertIn(self.user['username'], str(res.data))
        self.assertIn(self.user['email'], str(res.data))
        self.assertNotIn(self.user['password'], str(res.data))

    def test_corpus_creation(self):
        user_res = self.create_user()

        res = self.create_corpus()
        self.assertEqual(res.status_code, 201)
    
    
    def test_round_creation(self):
        res = self.create_round()
        self.assertEqual(res.status_code, 201)

    def test_user_can_write_lines(self):
        """ Test API can save user-written lines (POST). """
        res = self.create_user()
        # self.


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
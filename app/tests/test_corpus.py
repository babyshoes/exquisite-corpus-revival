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
        self.users = [
            {
                'name': 'Diane',
                'username': 'dianediane',
                'email': 'diane@diane.di',
                'password': 'Diane1sdiane'
            },
            {
                'name': 'Lee',
                'username': 'leandroid',
                'email': 'imabutt@lee.edu',
                'password': 'Le3L3eLe3'
            },
            # {
            #     'name': 'Steph',
            #     'username': 'steviewonder',
            #     'email': 'steph@stef.com',
            #     'password': 'step0nmeFungus'
            # }
        ]

        self.corpus = {
            'title': ''
        }

        with self.app.app_context():
            db.create_all()
            for user in self.users:
                # import pdb;pdb.set_trace()
                self.create_user(user)
            # import pdb;pdb.set_trace()
            self.poet_ids = [self.get_user_id(user) for user in self.users]

            self.starter_poet = self.poet_ids[0]
            self.create_corpus(self.starter_poet)

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
    
    def get_corpus_id(self, poet_id):
        data = {'poet_id': poet_id}
        corpus_info = self.client().get('/corpus/', data=data).data

        corpus_info = self.unpack_json(corpus_info)
        return int(corpus_info['id'])

    def unpack_json(self, json):
        output = re.findall(r"\{([\w\W]*)\}", str(json))[0]
        return dict([val.split(':') for val in output.replace('"', '').split(',')])

    # create corp
    def test_corpus_creation(self):
        """ Test API can create a corpus even before it's playable"""
        poet_id = self.poet_ids[0]
        res = self.create_corpus(poet_id)
        self.assertEqual(res.status_code, 201)

    def test_retrieve_corpus_id(self):
        """ Test API can retrieve corpus ID with initializer poet ID"""
        data = {'poet_id': self.starter_poet}
        res = self.client().get('/corpus/', data=data)

        corpus_info = self.unpack_json(res.data)
        
        self.assertEqual(res.status_code, 200)

    # def add_poets_to_corpus(self):
    #     """ Test API can add poets to already initialized corpus"""
    #     # add ids to corpus
    #     user_info = self.client().get('/poet/', data=self.user).data
    #     user_info = self.unpack_json(user_info)
    #     poet_id = int(user_info['id'])
    #     res = self.create_corpus(poet_id)

        # get corpus_id


    # def start_corpus(self):
    #    """ Test corpus is started upon >=3 poets join and initializer consent"""

    # def test_round_creation(self):
    #     res = self.create_round()
    #     self.assertEqual(res.status_code, 201)

    # def test_user_can_write_lines(self):
    #     """ Test API can save user-written lines (POST). """
    #     # self.


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
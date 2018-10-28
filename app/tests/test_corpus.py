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
                self.create_user(user)
            self.poet_ids = [self.get_user_id(user) for user in self.users]

            self.starter_poet = self.poet_ids[0]
            corpus_response = self.create_corpus().data
            self.corpus_id = int(self.unpack_json(corpus_response)['id'])
            # import pdb;pdb.set_trace()
            self.join_corpus_poet(self.starter_poet, self.corpus_id)

    def create_user(self, user_data):
        return self.client().post('/poet/', data=user_data)

    def get_user_id(self, user_data):
        user_info = self.client().get('/poet/', data=user_data).data
        user_info = self.unpack_json(user_info)
        return int(user_info['id'])

    def create_round(self):
        return self.client().post('/round/')

    def create_corpus(self):
        corpus_data = {**self.corpus}
        return self.client().post('/corpus/', data=corpus_data)
    
    def join_corpus_poet(self, poet_id, corpus_id, initializer=0):
        assc_data = {'poet_id': poet_id, 'corpus_id': corpus_id, 'initializer': initializer}
        return self.client().post('/corpus_poet/', data=assc_data)
    
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
        res = self.create_corpus()
        self.assertEqual(res.status_code, 201)

    def test_retrieve_corpus_id(self):
        """ Test API can retrieve corpus with ID"""
        data = {'id': self.corpus_id}
        res = self.client().get('/corpus/', data=data)
        # import pdb;pdb.set_trace()
        corpus_info = self.unpack_json(res.data)
        
        self.assertEqual(res.status_code, 200)

    # def add_starter_poet_to_corpus(self):
    #     """ Test API can add join initializing poet w/ their new corpus"""
    #     # add ids to corpus
    #     res = self.join_corpus_poet(self.starter_poet, self.corpus_id, True)
    #     self.assertEqual(res.status_code, 201)

    # def add_poets_to_corpus(self):
    #     """ Test API can add poets to already initialized corpus"""
    #     # add ids to corpus
    #     res = self.join_corpus_poet(self.starter_poet, self.corpus_id, True)
    #     self.assertEqual(res.status_code, 201)

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
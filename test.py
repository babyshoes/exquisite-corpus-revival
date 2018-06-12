import unittest
import os
import json
from app import app, db

class CorpusTestCase(unittest.TestCase):
    self.app = app
    self.client = app.test_client()

    with self.app.app_context():
        db.create_all()
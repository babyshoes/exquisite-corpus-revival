import os
# basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{pw}@db:5432/{db}".format(
        user=os.environ['POSTGRES_USER'],
        pw=os.environ['POSTGRES_PASSWORD'],
        db=os.environ['POSTGRES_DB']
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
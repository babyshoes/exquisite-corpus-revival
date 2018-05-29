from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

corpuses = db.Table('corpuses',
    db.Column('corpus_id', db.Integer, db.ForeignKey('corpus.id'), primary_key=True),
    db.Column('poet_id', db.Integer, db.ForeignKey('poet.id'), primary_key=True)
)

class Poet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128))
    corpuses = db.relationship('Corpus', secondary=corpuses, lazy='subquery',
        backref=db.backref('poets', lazy=True))
    lines = db.relationship('Line', backref='poet', lazy=True)

# each round must end w/ 2 lines
# a first round starts off w/ 0 lines
# all other rounds have prev rounds and start off w/ an exposed line, the secondline of prev round
class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    current = db.Column(db.Boolean, default=True)
    length = db.Column(db.Integer) # if corpus is timed, then length is prescriptive
    first_line = db.relationship('Line', backref='round', lazy=True) #maybe alias as exposed_line for number > 0
    second_line = db.relationship('Line', backref='round', lazy=True)
    start_time = db.Column(db.DateTime, nullable=False)
    completed_time = db.Column(db.DateTime, nullable=True)

class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    time_stamp = db.Column(db.DateTime, nullable=False)
    
class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rounds = db.relationship('Round', backref='poem')
    # current_round = db.relationship('CurrentRound', backref='poem', lazy=True)
    timed = db.Column(db.Boolean, unique=False, default=False)

class Corpus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    poems = db.relationship('Poem', backref='corpus', lazy=True)
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re
from extensions import db

corpus_poet = db.Table('corpus_poet',
    db.Column('corpus_id', db.Integer, db.ForeignKey('corpus.id'), primary_key=True),
    db.Column('poet_id', db.Integer, db.ForeignKey('poet.id'), primary_key=True),
    db.Column('initializer', db.Boolean, default=False)
)

class Poet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128))
    corpuses = db.relationship('Corpus', secondary=corpus_poet, lazy='subquery',
        backref=db.backref('poets', lazy=True))
    lines = db.relationship('Line', backref='poet', lazy=True)

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.set_password(password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def set_password(self, password):
        if not password:
            raise AssertionError('Password not provided')

        if not re.match('\d.*[A-Z]|[A-Z].*\d', password):
            raise AssertionError('Password must contain 1 capital letter and 1 number')

        if len(password) < 8 or len(password) > 50:
            raise AssertionError('Password must be between 8 and 50 characters')        
        
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password_hash, password)
    
    def lookup(self):
        atts = ['name', 'username', 'email', 'id']
        return {val: self.__dict__[val] for val in atts}


    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise AssertionError('No username provided')

        if Poet.query.filter(Poet.username == username).first():
            raise AssertionError('Username is already in use')

        if len(username) < 5 or len(username) > 20:
            raise AssertionError('Username must be between 5 and 20 characters')

        return username

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')
        
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError('Provided email is not an email address')

        return email
         
    @staticmethod
    def participated_in_corpuses(self):
        return self.corpuses
    
    def current_corpuses(self):
        pass

class Corpus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    started = db.Column(db.Boolean, default=False)
    poems = db.relationship('Poem', backref='corpus')
    # poets = db.relationship('Poet', secondary=corpus_poet, lazy='subquery',
    # backref=db.backref('corpuses', lazy=True))

    def __init__(self, title):
        self.title = title

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def lookup(self):
        atts = ['title', 'started', 'id']
        return {val: self.__dict__[val] for val in atts}

class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    corpus_id = db.Column(db.Integer, db.ForeignKey('corpus.id'), nullable=False)
    rounds = db.relationship('Round', backref='poem', lazy=True)
    # current_round = db.relationship('CurrentRound', backref='poem', lazy=True)
    timed = db.Column(db.Boolean, unique=False, default=False)
    
# each round must end w/ 2 lines
# a first round starts off w/ 0 lines
# all other rounds have prev rounds and start off w/ an exposed line, the secondline of prev round
class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poem_id = db.Column(db.Integer, db.ForeignKey('poem.id'), nullable=False)
    number = db.Column(db.Integer)
    current = db.Column(db.Boolean, default=True)
    length = db.Column(db.Integer) # if corpus is timed, then length is prescriptive
    first_line_id = db.Column(db.Integer, db.ForeignKey("line.id"))
    second_line_id = db.Column(db.Integer, db.ForeignKey("line.id"))
    first_line = db.relationship('Line', foreign_keys=[first_line_id], backref='roundAppearingAsPrompt', lazy=True) #maybe alias as exposed_line for number > 0
    second_line = db.relationship('Line', foreign_keys=[second_line_id], backref='roundWrittenIn', lazy=True)
    start_time = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    completed_time = db.Column(db.DateTime, nullable=True)

    def __init__(self, number):
        self.number = number

    def complete(self):
        self.current = False

class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poet_id = db.Column(db.Integer, db.ForeignKey('poet.id'), nullable=False)   
    content = db.Column(db.Text, nullable=False)
    time_stamp = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def __init__(self, content):
        self.content = content

    @validates('content')
    def validate_content(self, content):
        if not content:
            raise AssertionError('Write something!')


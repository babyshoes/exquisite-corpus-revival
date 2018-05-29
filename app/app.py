from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import *

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def for_starts():
    return "hello world"
    
if __name__ == 'main':
    app.run(debug=True, host='0.0.0.0')
from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def for_starts():
    return "hello world"
    
if __name__ == 'main':
    app.run(debug=True, host='0.0.0.0')
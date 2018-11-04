from flask import Flask, render_template, request, jsonify, abort
from config import Config
from extensions import *

def create_app():
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)
    from api.poets import poets_blueprint
    from api.corpuses import corpuses_blueprint
    from api.corpus_poets import corpus_poets_blueprint

    app.register_blueprint(poets_blueprint)
    app.register_blueprint(corpuses_blueprint)
    app.register_blueprint(corpus_poets_blueprint)
    
    return app

app = create_app()

@app.route('/')
def for_starts():
    return "hello world"
    
if __name__ == 'main':
    app.run(debug=True, host='0.0.0.0')

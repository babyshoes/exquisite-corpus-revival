from flask import Flask, render_template, request, jsonify, abort

from config import Config
from extensions import *
from models import *
from api.poets import poets_blueprint
from api.corpuses import corpuses_blueprint
from api.corpus_poets import corpus_poets_blueprint

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(poets_blueprint)
    app.register_blueprint(corpuses_blueprint)
    app.register_blueprint(corpus_poets_blueprint)

    # @app.route('/corpus_poet/', methods=['POST', 'GET'])
    # def post_corpus_poet():
    #     if request.method == "POST":
    #         data = request.data.items()
    #         statement = corpus_poet.insert().values(corpus_id=data['corpus_id'], 
    #                                                 poet_id=data['poet_id'])
    #         db.session.execute(statement)
    
    return app

app = create_app(Config)
migrate = Migrate(app, db)

@app.route('/')
def for_starts():
    return "hello world"
    
if __name__ == 'main':
    app.run(debug=True, host='0.0.0.0')

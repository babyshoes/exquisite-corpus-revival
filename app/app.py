from flask import Flask, render_template, request, jsonify, abort
from flask_api import FlaskAPI
from config import Config
from flask_migrate import Migrate
from models import *

def create_app(config_name):
    # app = Flask(__name__)
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route('/poet/', methods=['POST', 'GET'])
    def poets():
        username = str(request.data.get('username', ''))     
        data = request.data
         
        if request.method == "POST":
            if username:
                poet = Poet(**data.to_dict())
                poet.save()
                response = jsonify({
                    'name': poet.name,
                    'username': poet.username,
                    'email': poet.email,
                })
                response.status_code = 201
                return response
        else:
            # GET
            poet_info = Poet.query.filter_by(username=username).first().lookup()
            response = jsonify(poet_info)
            response.status_code = 200
            return response

    @app.route('/corpus/', methods=['POST', 'GET'])
    def corpuses():
        data = {k:v for k,v in request.data.iteritems() if k!='poets'}

        import pdb;pdb.set_trace()
        if request.method == "POST":
            corpus = Corpus(**data.to_dict())
            db.session.add([corpus])

            poet_ids = request.data['poets']
            if poet_ids:
                for poet_id in poet_ids:
                    statement = corpus_poet.insert().values(corpus_id=corpus.id, poet_id=poet_id)
                    db.session.execute(statement)
            
            db.session.commit()
            response = jsonify({
                'id': corpus.id,
                'title': corpus.title
            })
            response.status_code = 201
            return response

    return app

# app = Flask(__name__)
# app.config.from_object(Config)
# db.init_app(app)
app = create_app(Config)
migrate = Migrate(app, db)

@app.route('/')
def for_starts():
    return "hello world"
    
if __name__ == 'main':
    app.run(debug=True, host='0.0.0.0')

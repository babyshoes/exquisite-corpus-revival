from flask import Flask, render_template, request, jsonify, abort

from config import Config
from extensions import *
from models import *

def create_app(config_name):
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
        data = {k:v for k,v in request.data.items() if k!='poet_id'}
        poet_id = request.data['poet_id']

        if request.method == "POST":
            corpus = Corpus(**data)
            poet = Poet.query.filter_by(id=poet_id).first()
            corpus.poets.append(poet)
            corpus.save()
            # statement = corpus_poet.insert().values(corpus_id=corpus.id, poet_id=poet_id, initializer=True)
            # db.session.execute(statement)
            
            response = jsonify({
                'id': corpus.id,
                'title': corpus.title
            })
            response.status_code = 201
            return response
        else: # GET
            # TO DO: separate retrievals for corpuses initialized by poet
            # vs merely participated
            corpus_info = Poet.query.filter_by(id=poet_id).first().corpuses[0].lookup()
            # corpus_info = corpus_poet.query.filter_by(poet_id=poet_id)
            response = jsonify(corpus_info)
            response.status_code = 200
            return response


    @app.route('/corpus_poet/', methods=['POST', 'GET'])
    def post_corpus_poet():
        if request.method == "POST":
            data = request.data.items()
            statement = corpus_poet.insert().values(corpus_id=data['corpus_id'], 
                                                    poet_id=data['poet_id'])
            db.session.execute(statement)
    
    return app

app = create_app(Config)
migrate = Migrate(app, db)

@app.route('/')
def for_starts():
    return "hello world"
    
if __name__ == 'main':
    app.run(debug=True, host='0.0.0.0')

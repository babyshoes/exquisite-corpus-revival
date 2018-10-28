from flask import Blueprint, jsonify, request
from models import Corpus, Poet

corpuses_blueprint = Blueprint('corpuses', __name__)

@corpuses_blueprint.route('/corpus/', methods=['POST', 'GET'])
def corpuses():
    data = {k:v for k,v in request.data.items() if k!='id'}

    if request.method == "POST":
        corpus = Corpus(**data)
        corpus.save()
        
        response = jsonify({
            'id': corpus.id,
            'title': corpus.title
        })
        response.status_code = 201
        return response

    else: # GET
        # TO DO: separate retrievals for corpuses initialized by poet
        # vs merely participated
        corpus = Corpus.query.get(request.data['id'])

        response = jsonify({
            'id': corpus.id,
            'title': corpus.title
        })
        response.status_code = 200
        return response
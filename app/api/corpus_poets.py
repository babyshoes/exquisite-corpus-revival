from flask import Blueprint, jsonify, request
from models import CorpusPoet, Corpus, Poet
import json

corpus_poets_blueprint = Blueprint('corpus_poets', __name__)

@corpus_poets_blueprint.route('/corpus_poet/', methods=['POST', 'GET'])
def corpus_poet():
    data = request.data.to_dict()

    if request.method == 'POST':
        cp = CorpusPoet(**data)
        cp.save()

        response = jsonify({
            'id': cp.id
        })
        response.status_code = 201
        return response


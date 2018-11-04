from flask import Blueprint, jsonify, request
from models import CorpusPoet, CorpusPoetSchema, Corpus, Poet
import json

corpus_poets_blueprint = Blueprint('corpus_poets', __name__)
schema = CorpusPoetSchema()

@corpus_poets_blueprint.route('/corpus_poet/', methods=['POST', 'GET'])
def corpus_poet():
    cp_data = request.data.to_dict()

    if request.method == 'POST':
        cp = schema.load(cp_data).data
        import pdb;pdb.set_trace()
        cp.save()
        response = schema.jsonify(cp)

        response.status_code = 201
        return response

@corpus_poets_blueprint.route('/corpus_poet/<poet_id>', methods=['GET'])
def find_corpuses_by_poet_id(poet_id):
    corpus_schema = CorpusSchema()
    corpuses = Poet.get(poet_id).corpuses()
    return corpus_schema.jsonify(corpuses, many=True)


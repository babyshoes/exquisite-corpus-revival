from flask import Blueprint, jsonify, request
from models import Corpus, CorpusSchema

corpuses_blueprint = Blueprint('corpuses', __name__)

@corpuses_blueprint.route('/corpus/<id>', methods=['GET'])
def find_corpus_by_id(id):
    corpus = Corpus.query.get(id)
    return CorpusSchema().jsonify(corpus)

@corpuses_blueprint.route('/corpus/', methods=['POST'])
def post_corpus():
    corpus_data = request.data.to_dict()
    schema = CorpusSchema()
    
    corpus = schema.load(corpus_data).data
    corpus.save()

    return schema.jsonify(corpus)
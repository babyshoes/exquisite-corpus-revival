from flask import Blueprint, jsonify, request
from models import Poet, PoetSchema

poets_blueprint = Blueprint('poets', __name__)

@poets_blueprint.route('/poet/<id>', methods=['GET'])
def find_poet_by_id(id):
    poet = Poet.query.get(id)
    return PoetSchema().jsonify(poet)

@poets_blueprint.route('/poet/', methods=['POST'])
def post_poet():
    poet_data = request.data.to_dict()
    schema = PoetSchema()
    
    poet = schema.load(poet_data).data
    poet.save()

    return schema.jsonify(poet)

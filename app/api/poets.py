from flask import Blueprint, jsonify, request
from models import Poet

poets_blueprint = Blueprint('poets', __name__)

@poets_blueprint.route('/poet/', methods=['POST', 'GET'])
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
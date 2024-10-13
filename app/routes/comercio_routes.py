from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.comercio_services import get_comercio

comercio_bp = Blueprint('comercio', __name__)

@comercio_bp.route('/comercio', methods=['GET'])
@jwt_required()
def get_comercio_route():
    try:
        ano = request.args.get('ano', type=int)
        resultado = get_comercio(ano)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

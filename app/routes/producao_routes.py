from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.producao_services import get_producao

producao_bp = Blueprint('producao', __name__)

@producao_bp.route('/producao', methods=['GET'])
@jwt_required()
def get_producao_route():
    try:
        ano = request.args.get('ano', type=int)
        resultado = get_producao(ano)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

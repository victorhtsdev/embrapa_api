from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.processamento_services import get_processamento

processamento_bp = Blueprint('processamento', __name__)

@processamento_bp.route('/processamento/<objeto>', methods=['GET'])
@jwt_required()
def get_processamento_route(objeto):
    try:
        ano = request.args.get('ano', type=int)
        resultado = get_processamento(objeto, ano)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
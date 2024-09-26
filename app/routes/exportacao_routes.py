from flask import Blueprint, jsonify, request
from app.services.exportacao_services import get_exportacao

exportacao_bp = Blueprint('exportacao', __name__)

@exportacao_bp.route('/exportacao/<objeto>', methods=['GET'])
def get_exportacao_route(objeto):
    try:
        ano = request.args.get('ano', type=int)
        resultado = get_exportacao(objeto, ano)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
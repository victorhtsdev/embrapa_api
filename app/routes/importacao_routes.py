from flask import Blueprint, jsonify, request
from app.services.importacao_services import get_importacao

importacao_bp = Blueprint('importacao', __name__)

@importacao_bp.route('/importacao/<objeto>', methods=['GET'])
def get_importacao_route(objeto):
    try:
        ano = request.args.get('ano', type=int)
        resultado = get_importacao(objeto, ano)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
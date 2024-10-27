from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from app.services.producao_services import get_producao

producao_bp = Blueprint('producao', __name__)

@producao_bp.route('/producao', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Obter dados de Produção por Ano',
    'parameters': [
        {
            'name': 'ano',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'O ano para filtrar os dados de produção'
        }
    ],
    'responses': {
        200: {
            'description': 'Dados de produção recuperados com sucesso',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'uuid': {'type': 'string', 'description': 'O UUID do registro'},
                        'id': {'type': 'integer', 'description': 'O ID do registro'},
                        'control': {'type': 'string', 'description': 'Controle do registro'},
                        'produto': {'type': 'string', 'description': 'O produto'},
                        'ano': {'type': 'integer', 'description': 'O ano do registro'},
                        'quantidade': {'type': 'number', 'description': 'A quantidade produzida'},
                        'tipo': {'type': 'string', 'description': 'O tipo de produção'},
                        'totalizador': {'type': 'string', 'description': 'Totalizador do registro'}
                    }
                }
            }
        },
        401: {
            'description': 'Acesso não autorizado',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'description': 'Acesso não autorizado'
                    }
                },
                'example': {
                    'msg': 'Acesso não autorizado'
                }
            }
        },
        500: {
            'description': 'Erro interno do servidor',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def get_producao_route():
    try:
        ano = request.args.get('ano', type=int)
        resultado = get_producao(ano)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

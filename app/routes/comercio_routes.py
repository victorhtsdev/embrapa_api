from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.comercio_services import get_comercio
from flasgger import swag_from

comercio_bp = Blueprint('comercio', __name__)

@comercio_bp.route('/comercio', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Obter dados de comércio por ano',
    'parameters': [
        {
            'name': 'ano',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'O ano para filtrar os dados de comércio'
        }
    ],
    'responses': {
        200: {
            'description': 'Dados de comércio recuperados com sucesso',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'uuid': {
                            'type': 'string',
                            'description': 'O UUID do registro'
                        },
                        'id': {
                            'type': 'integer',
                            'description': 'O ID do registro'
                        },
                        'control': {
                            'type': 'string',
                            'description': 'Controle do registro'
                        },
                        'produto': {
                            'type': 'string',
                            'description': 'O produto'
                        },
                        'ano': {
                            'type': 'integer',
                            'description': 'O ano do registro'
                        },
                        'quantidade': {
                            'type': 'number',
                            'description': 'A quantidade comercializada'
                        },
                        'tipo': {
                            'type': 'string',
                            'description': 'O tipo de comércio'
                        },
                        'totalizador': {
                            'type': 'string',
                            'description': 'Totalizador do registro'
                        }
                    }
                }
            }
        },
        401: {
            'description': 'Acesso não Autorizado',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'description': 'Acesso Não Autorizado'
                    }
                },
                'example': {
                    'msg': 'Acesso não Autorizado'
                }
            }
        },
        500: {
            'description': 'Erro interno do servidor',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Mensagem de erro'
                    }
                }
            }
        }
    }
})
def get_comercio_route():
    try:
        ano = request.args.get('ano', type=int)
        resultado = get_comercio(ano)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

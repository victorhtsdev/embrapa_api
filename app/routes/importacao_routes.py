from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from app.services.importacao_services import get_importacao

importacao_bp = Blueprint('importacao', __name__)

@importacao_bp.route('/importacao/<objeto>', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Obter dados de Importação por Ano',
    'security': [{"BearerAuth": []}],
    'parameters': [
        {
            'name': 'objeto',
            'in': 'path',
            'type': 'string',
            'required': True,
            'enum': [
                'importacaoVinhoMesa',
                'importacaoEspumantes',
                'importacaoUvasFrescas',
                'importacaoUvasPassas',
                'importacaoSuco'
            ],
            'description': (
                    'Opções da aba Importação do site da Embrapa:<br>'
                    '<b>importacaoVinhoMesa</b> - Vinhos de Mesa<br>'
                    '<b>importacaoEspumantes</b> - Espumantes<br>'
                    '<b>importacaoUvasFrescas</b> - Uvas Frescas<br>'
                    '<b>importacaoUvasPassas</b> - Uvas Passas<br>'
                    '<b>importacaoSuco</b> - Suco de Uva<br><br>'
            )
        },
        {
            'name': 'ano',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Ano da importação'
        },
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer {token}'
        }
    ],
    'responses': {
        200: {
            'description': 'Resposta bem-sucedida',
            'schema': {
                'type': 'object',
                'properties': {
                    'last_uuid': {'type': 'string'},
                    'record_date': {'type': 'string'},
                    'object_modified_data': {'type': 'string'},
                    'importacao': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'ano': {'type': 'string'},
                                'objeto': {'type': 'string'},
                                'quantidade_total': {'type': 'number'},
                                'valor_total': {'type': 'number'},
                                'paises': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'pais': {'type': 'string'},
                                            'quantidade_pais': {'type': 'number'},
                                            'valor_pais': {'type': 'number'}
                                        }
                                    }
                                }
                            }
                        }
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
def get_importacao_route(objeto):
    try:
        ano = request.args.get('ano', type=int)
        resultado = get_importacao(objeto, ano)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
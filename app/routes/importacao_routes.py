from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from app.services.importacao_services import get_importacao

importacao_bp = Blueprint('importacao', __name__)

@importacao_bp.route('/importacao/<objeto>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dados Vinicultura Embrapa'],
    'summary': 'Obter dados de Importação por Ano',
    'security': [{"BearerAuth": []}],
    'operationId': 'Importação',
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
                    'last_uuid': {
                        'type': 'string',
                        'description': 'O UUID do último registro'
                    },
                    'record_date': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'Data e hora do registro'
                    },
                    'object_modified_data': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'Data e hora da última modificação do objeto'
                    },
                    'importacao': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'ano': {
                                    'type': 'string',
                                    'description': 'Ano da importação'
                                },
                                'objeto': {
                                    'type': 'string',
                                    'description': 'Objeto de importação'
                                },
                                'quantidade_total': {
                                    'type': 'number',
                                    'description': 'Quantidade total importada'
                                },
                                'valor_total': {
                                    'type': 'number',
                                    'description': 'Valor total importado'
                                },
                                'paises': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'pais': {
                                                'type': 'string',
                                                'description': 'Nome do país'
                                            },
                                            'quantidade_pais': {
                                                'type': 'number',
                                                'description': 'Quantidade importada pelo país'
                                            },
                                            'valor_pais': {
                                                'type': 'number',
                                                'description': 'Valor importado pelo país'
                                            }
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
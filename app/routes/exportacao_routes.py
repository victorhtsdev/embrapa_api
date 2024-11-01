from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from app.services.exportacao_services import get_exportacao

exportacao_bp = Blueprint('exportacao', __name__)

@exportacao_bp.route('/exportacao/<objeto>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dados Vinicultura Embrapa'],
    'summary': 'Obter dados de Exportação por Ano',
    'security': [{"BearerAuth": []}],
    'operationId': 'Exportação',
    'parameters': [
        {
            'name': 'objeto',
            'in': 'path',
            'type': 'string',
            'required': True,
            'enum': [
                'exportacaoVinhoMesa',
                'exportacaoEspumantes',
                'exportacaoUvasFrescas',
                'exportacaoSuco'
            ],
            'description': (
                'Opções da aba Exportação do site da Embrapa:<br>'
                '<b>exportacaoVinhoMesa</b> - Vinhos de Mesa<br>'
                '<b>exportacaoEspumantes</b> - Espumantes<br>'
                '<b>exportacaoUvasFrescas</b> - Uvas Frescas<br>'
                '<b>exportacaoSuco</b> - Suco de Uva<br><br>'
            )
        },
        {
            'name': 'ano',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Ano da exportação'
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
                    'exportacao': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'ano': {
                                    'type': 'string',
                                    'description': 'Ano da exportação'
                                },
                                'objeto': {
                                    'type': 'string',
                                    'description': 'Objeto de exportação'
                                },
                                'quantidade_total': {
                                    'type': 'number',
                                    'description': 'Quantidade total exportada'
                                },
                                'valor_total': {
                                    'type': 'number',
                                    'description': 'Valor total exportado'
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
                                                'description': 'Quantidade exportada para o país'
                                            },
                                            'valor_pais': {
                                                'type': 'number',
                                                'description': 'Valor exportado para o país'
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
def get_exportacao_route(objeto):
    try:
        ano = request.args.get('ano', type=int)
        resultado = get_exportacao(objeto, ano)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
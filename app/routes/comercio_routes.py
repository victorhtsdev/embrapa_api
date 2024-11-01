from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.comercio_services import get_comercio
from flasgger import swag_from

comercio_bp = Blueprint('comercio', __name__)

@comercio_bp.route('/comercio', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dados Vinicultura Embrapa'],
    'summary': 'Obter dados de Comercialização por ano',
    'security': [{"BearerAuth": []}],
    'operationId': 'Comercialização',
    'parameters': [
        {
            'name': 'ano',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'O ano para filtrar os dados de comércio'
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
            'description': 'Dados de comércio recuperados com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'comercio': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'ano': {
                                    'type': 'string',
                                    'description': 'Ano do registro de comércio'
                                },
                                'quantidade_litros_total': {
                                    'type': 'string',
                                    'description': 'Quantidade total de litros comercializados'
                                },
                                'tipos': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'tipo_produto': {
                                                'type': 'string',
                                                'description': 'Tipo de produto comercializado'
                                            },
                                            'quantidade_litros_tipo': {
                                                'type': 'string',
                                                'description': 'Quantidade de litros para o tipo de produto'
                                            },
                                            'itens': {
                                                'type': 'array',
                                                'items': {
                                                    'type': 'object',
                                                    'properties': {
                                                        'produto': {
                                                            'type': 'string',
                                                            'description': 'Nome do produto'
                                                        },
                                                        'quantidade_litros_produto': {
                                                            'type': 'string',
                                                            'description': 'Quantidade de litros do produto'
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
                    'last_uuid': {
                        'type': 'string',
                        'description': 'O UUID do último registro'
                    },
                    'object_modified_data': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'Data e hora da última modificação do objeto'
                    },
                    'record_date': {
                        'type': 'string',
                        'format': 'date-time',
                        'description': 'Data e hora do registro'
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

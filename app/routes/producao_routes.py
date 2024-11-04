from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from app.services.producao_services import get_producao

producao_bp = Blueprint('producao', __name__)

@producao_bp.route('/producao', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dados Vinicultura Embrapa'],
    'summary': 'Obter dados de Produção por Ano',
    'security': [{"BearerAuth": []}],
    'operationId': 'Produção',
    'parameters': [
        {
            'name': 'ano',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'O ano para filtrar os dados de produção'
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
            'description': 'Dados de produção recuperados com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'last_uuid': {'type': 'string', 'description': 'O último UUID processado'},
                    'object_modified_data': {'type': 'string', 'description': 'Data de modificação do objeto'},
                    'record_date': {'type': 'string', 'description': 'Data do registro'},
                    'producao': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'ano': {'type': 'string', 'description': 'Ano do processamento'},
                                'quantidade_total_litros': {'type': 'string', 'description': 'Quantidade total em litros'},
                                'tipos': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'tipo_produto': {'type': 'string', 'description': 'Tipo de produto'},
                                            'quantidade_tipo_litros': {'type': 'string',
                                                                   'description': 'Quantidade total do tipo em litros'},
                                            'itens': {
                                                'type': 'array',
                                                'items': {
                                                    'type': 'object',
                                                    'properties': {
                                                        'produto': {'type': 'string', 'description': 'Nome do produto'},
                                                        'quantidade_produto_litros': {'type': 'string',
                                                                                  'description': 'Quantidade do produto em litros'}
                                                    }
                                                }
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
def get_producao_route():
    try:
        ano = request.args.get('ano', type=int)
        resultado = get_producao(ano)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

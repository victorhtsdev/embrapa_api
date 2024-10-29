from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from app.services.processamento_services import get_processamento

processamento_bp = Blueprint('processamento', __name__)

@processamento_bp.route('/processamento/<objeto>', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Obter dados de Processamento por Ano',
    'parameters': [
        {
            'name': 'objeto',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': (
                    'Opções da aba Processamento do site da Embrapa.<br>'
                    '<b>processamentoViniferas</b> - Viníferas<br>'
                    '<b>processamentoAmericanas</b> - Americanas e Híbridas<br>'
                    '<b>processamentoUvaMesa</b> - Uvas de Mesa<br>'
                    '<b>processamentoSemClass</b> - Sem Classificação<br><br>'
            )
        },
        {
            'name': 'ano',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'O ano para filtrar os dados de processamento'
        }
    ],
    'responses': {
        200: {
            'description': 'Dados de processamento recuperados com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'last_uuid': {'type': 'string', 'description': 'O último UUID processado'},
                    'record_date': {'type': 'string', 'description': 'Data do registro'},
                    'object_modified_data': {'type': 'string', 'description': 'Data de modificação do objeto'},
                    'processamento': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'ano': {'type': 'string', 'description': 'Ano do processamento'},
                                'quantidade_total_kg': {'type': 'number', 'description': 'Quantidade total em kg'},
                                'tipos': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'tipo_cultivar': {'type': 'string', 'description': 'Tipo de cultivar'},
                                            'itens': {
                                                'type': 'array',
                                                'items': {
                                                    'type': 'object',
                                                    'properties': {
                                                        'cultivar': {'type': 'string', 'description': 'Cultivar'},
                                                        'quantidade_cultivar_kg': {'type': 'number', 'description': 'Quantidade do cultivar em kg'}
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
def get_processamento_route(objeto):
    try:
        ano = request.args.get('ano', type=int)
        resultado = get_processamento(objeto, ano)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
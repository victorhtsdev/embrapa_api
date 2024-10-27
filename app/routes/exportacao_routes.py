from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from app.services.exportacao_services import get_exportacao

exportacao_bp = Blueprint('exportacao', __name__)

@exportacao_bp.route('/exportacao/<objeto>', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Obter dados de Exportação por Ano',
    'parameters': [
        {
            'name': 'objeto',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Objeto/Tipo de Uva de exportação'
        },
        {
            'name': 'ano',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Ano da exportação'
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
                    'exportacao': {
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
def get_exportacao_route(objeto):
    try:
        ano = request.args.get('ano', type=int)
        resultado = get_exportacao(objeto, ano)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
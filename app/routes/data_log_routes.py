from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from flasgger import swag_from

from app.services.data_log_services import get_data_log_by_uuid

data_log_bp = Blueprint('data_info', __name__)

@data_log_bp.route('/data_info/<string:uuid>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Dados Vinicultura Embrapa'],
    'summary': 'Obter os dados e metadados da captura no site da Embrapa, (Versionamento do CSV de Download)',
    'security': [{"BearerAuth": []}],
    'operationId': 'Log',
    'parameters': [
        {
            'name': 'uuid',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'UUID de controle de dados'
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
            'description': 'Log de dados recuperado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'data_source': {'type': 'string', 'description': 'Dados fonte codificados em base64'},
                    'object': {'type': 'string', 'description': 'Tipo de objeto'},
                    'object_modified_date': {'type': 'string', 'description': 'Data de modificação do objeto'},
                    'record_date': {'type': 'string', 'description': 'Data de registro'},
                    'uuid': {'type': 'string', 'description': 'UUID do registro'}
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
        404: {
            'description': 'Log de dados não encontrado',
            'examples': {
                'application/json': {
                    'error': 'Log de dados não encontrado'
                }
            }
        },
        500: {
            'description': 'Erro interno do servidor',
            'examples': {
                'application/json': {
                    'error': 'Erro interno do servidor'
                }
            }
        }
    }
})
def get_data_log_by_uuid_route(uuid):
    try:
        resultado = get_data_log_by_uuid(uuid)
        return jsonify(resultado), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
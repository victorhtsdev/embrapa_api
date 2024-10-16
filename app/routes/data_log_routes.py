from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.data_log_services import get_data_log_by_uuid

data_log_bp = Blueprint('data_info', __name__)

@data_log_bp.route('/data_info/<string:uuid>', methods=['GET'])
@jwt_required()
def get_data_log_by_uuid_route(uuid):
    try:
        resultado = get_data_log_by_uuid(uuid)
        return jsonify(resultado), 200
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.services.usuario_service import check_usuario
from app.services.usuario_service import create_usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = check_usuario(username, password)

    if user:
        access_token = create_access_token(identity=user.usuario)
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Credenciais inválidas"}), 401


@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"error": "Username e senha são obrigatórios"}), 400

    user = create_usuario(username, password)

    if user:
        return jsonify({"msg": "Usuário cadastrado com sucesso"}), 201
    return jsonify({"error": "Usuário já existe"}), 409
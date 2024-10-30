from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.services.usuario_service import check_usuario
from app.services.usuario_service import create_usuario
from flasgger import swag_from

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'summary': 'Login, gerar Bearer Token',
    'operationId': 'Login',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'description': 'O Username do Usuário'},
                    'password': {'type': 'string', 'description': 'A Senha do Usuário'}
                }
            },
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'examples': {
                'application/json': {
                    'access_token': 'string'
                }
            }
        },
        401: {
            'description': 'Invalid credentials',
            'examples': {
                'application/json': {
                    'msg': 'Credenciais inválidas'
                }
            }
        }
    },
})
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = check_usuario(username, password)

    if user:
        access_token = create_access_token(identity=user.usuario)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Credenciais inválidas"}), 401


@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'summary': 'Registro de Usuários',
    'operationId': 'Usuários',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'description': 'O Username do Usuário'},
                    'password': {'type': 'string', 'description': 'A Senha do Usuário'}
                }
            },
        }
    ],
    'responses': {
        201: {
            'description': 'User registered successfully',
            'examples': {
                'application/json': {
                    'msg': 'Usuário cadastrado com sucesso'
                }
            }
        },
        400: {
            'description': 'Username and password are required',
            'examples': {
                'application/json': {
                    'msg': 'Username e senha são obrigatórios'
                }
            }
        },
        409: {
            'description': 'User already exists',
            'examples': {
                'application/json': {
                    'msg': 'Usuário já existe'
                }
            }
        }
    },
})
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"msg": "Username e senha são obrigatórios"}), 400

    user = create_usuario(username, password)

    if user:
        return jsonify({"msg": "Usuário cadastrado com sucesso"}), 201
    return jsonify({"msg": "Usuário já existe"}), 409
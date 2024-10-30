from flask import Flask
from flask_jwt_extended import JWTManager
from app.extensions import db
from app.routes.auth_routes import auth_bp
from app.routes.comercio_routes import comercio_bp
from app.routes.exportacao_routes import exportacao_bp
from app.routes.importacao_routes import importacao_bp
from app.routes.processamento_routes import processamento_bp
from app.routes.producao_routes import producao_bp
from app.routes.data_log_routes import data_log_bp
from app.management.scheduled_tasks import start_scheduler, run_embrapa_task
from dotenv import load_dotenv
import os
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config.from_object('app.config.Config')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    db.init_app(app)
    JWTManager(app)

    swagger_config = {
        "title": "Embrapa API - POS TECH FIAP",
        "description": "API para obter os dados de Produção, Processamento, Comercialização, Importação e Exportação da Embrapa.",
        "version": "1.0.0",
        "termsOfService": "/terms",
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
        "headers": []
    }


    Swagger(app, config=swagger_config)


    app.register_blueprint(producao_bp, url_prefix='/api')
    app.register_blueprint(data_log_bp, url_prefix='/api')
    app.register_blueprint(exportacao_bp, url_prefix='/api')
    app.register_blueprint(importacao_bp, url_prefix='/api')
    app.register_blueprint(comercio_bp, url_prefix='/api')
    app.register_blueprint(processamento_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')

    with app.app_context():
        try:
            start_scheduler(app)
        except Exception:
            pass

    return app

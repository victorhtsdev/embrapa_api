from flask import Flask
from app.extensions import db
from app.routes.exportacao_routes import exportacao_bp
from app.routes.importacao_routes import importacao_bp
from app.routes.producao_routes import producao_bp
from app.routes.data_log_routes import data_log_bp
from app.management.scheduled_tasks import start_scheduler, run_embrapa_task

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)

    app.register_blueprint(producao_bp, url_prefix='/api')
    app.register_blueprint(data_log_bp, url_prefix='/api')
    app.register_blueprint(exportacao_bp, url_prefix='/api')
    app.register_blueprint(importacao_bp, url_prefix='/api')

    with app.app_context():
        try:
            start_scheduler(app)
        except Exception:
            pass

    return app

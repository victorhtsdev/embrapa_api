import atexit
from flask import current_app
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.data_log_services import get_data_from_embrapa

def run_embrapa_task(app):
    with app.app_context():
        try:
            get_data_from_embrapa('producao')
            get_data_from_embrapa('exportacaoUva')
            get_data_from_embrapa('exportacaoEspumantes')
            get_data_from_embrapa('exportacaoVinhoMesa')
        except Exception as e:
            pass

def start_scheduler(app):
    scheduler = BackgroundScheduler()

    scheduler.add_job(func=lambda: run_embrapa_task(app), trigger="interval", seconds=10)

    run_embrapa_task(app)

    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())

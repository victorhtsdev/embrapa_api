import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.data_log_services import get_data_from_embrapa


def run_embrapa_task():
    try:
        get_data_from_embrapa('producao')
        get_data_from_embrapa('exportacaoUva')
        get_data_from_embrapa('exportacaoEspumantes')
        get_data_from_embrapa('exportacaoVinhoMesa')

    except Exception as e:
        pass

def start_scheduler():
    scheduler = BackgroundScheduler()


    scheduler.add_job(func=run_embrapa_task, trigger="interval", seconds=10)

    run_embrapa_task()

    scheduler.start()

    #Para o agendador
    atexit.register(lambda: scheduler.shutdown())
import atexit
from datetime import datetime, timedelta
from apscheduler.triggers.date import DateTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.data_log_services import get_data_from_embrapa


def run_embrapa_task(app):
    with app.app_context():
        objetos = ['producao', 'exportacaoEspumantes', 'exportacaoVinhoMesa', 'exportacaoUvasFrescas', 'exportacaoSuco',
                   'importacaoEspumantes', 'importacaoVinhoMesa', 'importacaoUvasFrescas', 'importacaoSuco',
                   'importacaoPassas','comercio', 'processamentoViniferas','processamentoAmericanas','processamentoUvaMesa','processamentoSemClass']

        for objeto in objetos:
            try:
                get_data_from_embrapa(objeto)
            except Exception as e:
                continue
def start_scheduler(app):
    scheduler = BackgroundScheduler()

    scheduler.add_job(func=lambda: run_embrapa_task(app), trigger="interval", hours=12)

    start_time = datetime.now() + timedelta(minutes=1)
    scheduler.add_job(func=lambda: run_embrapa_task(app), trigger=DateTrigger(run_date=start_time))


    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())

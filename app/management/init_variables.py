from app.models.data_log import DataLog
from app.extensions import db

def get_latest_record_by_object(object_value):
    try:
        record = db.session.query(DataLog).filter_by(object=object_value).order_by(DataLog.record_date.desc()).first()
        if record:
            return record
        else:
            print(f"Nenhum registro encontrado para o objeto: {object_value}")
            return None
    except Exception as e:
        print(f"Erro ao buscar registro: {e}")
        return None